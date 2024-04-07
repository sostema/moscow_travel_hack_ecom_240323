from fastapi import APIRouter, Cookie, Header, HTTPException, Request, Response, status
from presentation.dependencies import container
from schemas.base import CamelizedBaseModel
from schemas.message import Message, Messages
from service.chat_service import HistoryNotFound

router = APIRouter(prefix="/gigachat")


class UserMessage(CamelizedBaseModel):
    content: str


@router.post("/messages")
def send_message(
    response: Response,
    prompt: UserMessage = UserMessage(content="Привет, как дела?"),
    history_id: str | None = Cookie(None),
) -> Message:
    """
    Отправляет промпт в гигачат. Возвращает X-History-Id, который можно использовать для консистентности истории.
    """
    try:
        chat_response, history_id = container.chat_service.send_message(
            prompt.content, history_id=history_id
        )
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound

    response.set_cookie(key="history_id", value=history_id)

    return chat_response


@router.post("/messages/history")
def get_history(history_id: str | None = Cookie(None)) -> Messages:
    """
    Возвращает историю сообщений по ID
    """
    if history_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="history id required",
        )

    try:
        history = container.chat_service.get_history(history_id=history_id)
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound

    return history


@router.delete("/messages/history")
def reset_history(response: Response, history_id: str | None = Cookie(None)) -> None:
    """
    Возвращает историю сообщений по ID
    """
    if history_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="history id required",
        )

    response.delete_cookie(key="history_id")

    return None


@router.post("/messages/history/all")
def get_all_histories() -> list[str]:
    """
    Возвращает айди всех историй. Только для отладки
    """

    return container.chat_service.get_all_histories()


@router.post("/search")
def search(
    response: Response,
    prompt: UserMessage = UserMessage(content="Что покушать?"),
) -> Message:
    """
    Возвращает айди всех историй. Только для отладки
    """

    message, history_id = container.chat_service.search(prompt.content)
    response.set_cookie(key="history_id", value=history_id)

    return message

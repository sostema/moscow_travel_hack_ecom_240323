from fastapi import APIRouter, Cookie, Header, HTTPException, Request, Response, status
from presentation.dependencies import container
from schemas.base import CamelizedBaseModel
from service.chat_service import HistoryNotFound, Message

router = APIRouter(prefix="/gigachat")


class Prompt(CamelizedBaseModel):
    text: str


@router.post("/messages")
def send_message(
    response: Response,
    prompt: Prompt = Prompt(text="Привет, как дела?"),
    history_id: str | None = Cookie(None),
) -> Prompt:
    """
    Отправляет промпт в гигачат. Возвращает X-History-Id, который можно использовать для консистентности истории.
    """
    try:
        chat_response, history_id = container.chat_service.send_message(
            prompt.text, history_id=history_id
        )
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound

    response.set_cookie(key="history_id", value=history_id)

    return Prompt(text=chat_response)


@router.post("/messages/history")
def get_history(history_id: str | None = Cookie(None)) -> list[Message]:
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


@router.post("/messages/history/all")
def get_all_histories() -> list[str]:
    """
    Возвращает айди всех историй. Только для отладки
    """

    return container.chat_service.get_all_histories()

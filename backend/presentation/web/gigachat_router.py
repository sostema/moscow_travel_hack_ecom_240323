from fastapi import APIRouter, Header, HTTPException, Response, status
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
    history_id: str | None = Header(None, alias="X-History-Id"),
) -> Prompt:
    """
    Отправляет промпт в гигачат. Возвращает X-History-Id, который можно использовать для консистентности истории.
    """
    if history_id is not None:
        response.headers["X-History-Id"] = history_id

    try:
        chat_response, history_id = container.chat_service.send_message(
            prompt.text, history_id=history_id
        )
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound
    response.headers["X-History-Id"] = history_id

    return Prompt(text=chat_response)


@router.post("/messages/history")
def send_message(
    response: Response,
    history_id: str = Header(..., alias="X-History-Id"),
) -> list[Message]:
    """
    Возвращает историю сообщений по ID
    """

    try:
        history = container.chat_service.get_history(history_id=history_id)
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound
    response.headers["X-History-Id"] = history_id

    return history


@router.post("/messages/history/all")
def get_all_histories() -> list[str]:
    """
    Возвращает айди всех историй. Только для отладки
    """

    return container.chat_service.get_all_histories()

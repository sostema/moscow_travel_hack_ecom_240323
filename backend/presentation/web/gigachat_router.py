from fastapi import APIRouter, Header, HTTPException, Response, status
from presentation.dependencies import container
from schemas.base import CamelizedBaseModel
from service.chat_service import HistoryNotFound

router = APIRouter(prefix="/gigachat")


class Prompt(CamelizedBaseModel):
    text: str


@router.post("/prompt")
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

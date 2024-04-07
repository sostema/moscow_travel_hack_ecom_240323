from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from presentation.dependencies import container
from schemas.base import CamelizedBaseModel
from schemas.message import Message, Messages
from service.chat_service import HistoryNotFound
from shared.base import logger

router = APIRouter(prefix="/gigachat")


class UserMessage(CamelizedBaseModel):
    content: str


def get_history_id_with_stop(
    response: Response,
    history_id: str | None = Cookie(None),
    prompt: UserMessage = UserMessage(content="Что покушать?"),
) -> str | None:
    if history_id is None:
        return history_id

    logger.debug("processing history id: {}", history_id)

    if not prompt.content.lower().startswith(("стоп", "заново", "забудь")):
        return history_id

    response.delete_cookie(key="history_id")
    logger.debug("history id: {} removed via get_history_id_with_stop", history_id)
    return None


@router.post("/messages", response_model_exclude_none=True)
def send_message(
    response: Response,
    prompt: UserMessage = UserMessage(content="Привет, как дела?"),
    history_id: str | None = Depends(get_history_id_with_stop),
) -> Message:
    """
    Отправляет промпт в гигачат. В кукизах сохраняется ID истории.
    Отправка слова "стоп" вначале промпта удалит историю
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


@router.get("/messages/history", response_model_exclude_none=True)
def get_history(
    history_id: str | None = Cookie(None),
    remove_system: bool = Query(True, alias="removeSystem"),
) -> Messages:
    """
    Возвращает историю сообщений по ID
    """
    if history_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="history id required",
        )

    try:
        history = container.chat_service.get_history(
            history_id=history_id, remove_system=remove_system
        )
    except HistoryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="history not found"
        ) from HistoryNotFound

    return history


@router.delete("/messages/history", response_model_exclude_none=True)
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


@router.get("/messages/history/all", response_model_exclude_none=True)
def get_all_histories() -> list[str]:
    """
    Возвращает айди всех историй. Только для отладки
    """

    return container.chat_service.get_all_histories()


@router.post("/search", response_model_exclude_none=True)
def search(
    response: Response,
    prompt: UserMessage = UserMessage(content="Что покушать?"),
    history_id: str | None = Depends(get_history_id_with_stop),
) -> Message:
    """
    Поиск места или события
    Отправка слова "стоп" вначале промпта удалит историю
    """
    if history_id is not None:
        return container.chat_service.search_continue(prompt.content, history_id)

    message, history_id = container.chat_service.search(prompt.content)
    response.set_cookie(key="history_id", value=history_id)

    return message

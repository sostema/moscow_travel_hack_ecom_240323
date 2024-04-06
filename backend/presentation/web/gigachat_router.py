import enum

from fastapi import APIRouter, Header, Response, status
from fastapi.responses import UJSONResponse
from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from schemas.base import CamelizedBaseModel
from shared.base import logger

router = APIRouter(prefix="/gigachat")


class Prompt(CamelizedBaseModel):
    prompt: str


@router.post("/prompt")
def send_message(
    response: Response,
    prompt: Prompt,
    history_id: str | None = Header(None, alias="X-History-Id"),
) -> str:
    if history_id is not None:
        response.headers["X-History-Id"] = history_id

    chat_response, history_id = container.chat_service.send_message(
        prompt.prompt, history_id=history_id
    )
    response.headers["X-History-Id"] = history_id

    return chat_response

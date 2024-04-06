import enum

from fastapi import APIRouter, status
from fastapi.responses import UJSONResponse
from presentation.dependencies import container
from presentation.web.schemas import HealthResponse, HealthStatuses
from shared.base import logger

router = APIRouter(prefix="gigachat")


@router.post("prompt")
def send_message(prompt: str) -> str:
    return container.chat_service.send_message(prompt)

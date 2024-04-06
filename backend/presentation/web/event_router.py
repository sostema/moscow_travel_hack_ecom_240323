from fastapi import APIRouter
from presentation.web.examples import events
from schemas.event import Event

router = APIRouter(prefix="/events")


@router.get("", response_model_exclude_none=True)
async def get_events() -> list[Event]:
    return events

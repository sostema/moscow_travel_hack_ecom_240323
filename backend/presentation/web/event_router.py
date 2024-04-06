from fastapi import APIRouter
from schemas.event import Events, example_events

router = APIRouter(prefix="/events")


@router.get("", response_model_exclude_none=True, response_model=Events)
async def get_events() -> Events:
    return Events(events=example_events)

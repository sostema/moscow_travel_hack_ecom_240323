from fastapi import APIRouter
from presentation.dependencies import container
from schemas.event import Events, Route, example_events

router = APIRouter(prefix="/events")


@router.get("", response_model_exclude_none=True, response_model=Events)
async def get_events() -> Events:
    return container.event_service.get_events()


@router.get("/routes", response_model_exclude_none=True, response_model=Route)
async def get_routes() -> Route:
    return Route(
        events=container.event_service.get_events().events[:6], time=500, distance=4.2
    )
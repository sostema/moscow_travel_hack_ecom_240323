from fastapi import APIRouter
from presentation.dependencies import container
from schemas.event import Event, Events, EventType, Route, example_events

router = APIRouter(prefix="/events")


@router.get("", response_model_exclude_none=True, response_model=Events)
async def get_events() -> Events:
    return container.event_service.get_events()


@router.get("/routes", response_model_exclude_none=True, response_model=Route)
async def get_routes() -> Route:
    events = container.event_service.get_events().events
    return Route(
        events=[
            events[0],
            Event(
                type=EventType.WALK,
                name="WALK",
                description="",
                link="",
                price=0,
                time=32 * 60,
                distance=2.500,
            ),
            events[1],
            Event(
                type=EventType.WALK,
                name="WALK",
                description="",
                link="",
                price=0,
                time=20 * 60,
                distance=2.1,
            ),
            events[2],
            Event(
                type=EventType.WALK,
                name="WALK",
                description="",
                link="",
                price=0,
                time=12 * 60,
                distance=1.2,
            ),
            events[3],
        ],
        time=64 * 60,
        distance=5.8,
    )

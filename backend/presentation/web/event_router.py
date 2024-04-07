import random
import uuid

from fastapi import APIRouter
from presentation.dependencies import container
from schemas.event import Event, Events, EventType, Route, example_events

router = APIRouter(prefix="/events")


@router.get(
    "",
    response_model_exclude_none=True,
    response_model_by_alias=True,
    response_model=Events,
)
async def get_events() -> Events:
    return Events(
        events=random.choices(container.event_service.get_events().events, k=6)
    )


@router.get(
    "/routes",
    response_model_exclude_none=True,
    response_model_by_alias=True,
    response_model=Route,
)
async def get_routes() -> Route:
    events_dict = container.event_service.get_events().id_to_event()

    return Route(
        events=[
            events_dict[uuid.UUID("018eb7f5-91b5-c150-e663-bc5e9942de2a")],
            Event(
                type=EventType.WALK,
                name="WALK",
                description="",
                link="",
                price=0,
                time=32 * 60,
                distance=2.500,
            ),
            events_dict[uuid.UUID("018eb7f5-8394-6a29-edaf-74180659acbe")],
            Event(
                type=EventType.WALK,
                name="WALK",
                description="",
                link="",
                price=0,
                time=20 * 60,
                distance=2.1,
            ),
            events_dict[uuid.UUID("018eb7f5-7f46-2325-5170-8f310332fe03")],
        ],
        time=64 * 60,
        distance=5.8,
    )

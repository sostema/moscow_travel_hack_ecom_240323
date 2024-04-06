import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic import Field
from schemas.base import CamelizedBaseModel


class EventType(StrEnum):
    RESTAURANTS = "RESTAURANTS"
    EVENT = "EVENT"
    WALK = "WALK"


# TODO rename to more meaningfull name
class TimeDistance(CamelizedBaseModel):
    time: int = Field(..., description="in seconds")
    distance: float = Field(..., description="in KM")


class Event(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    type_: EventType = Field(..., alias="type")
    name: str | None = None
    description: str | None = None
    link: str | None = None
    img_link: str | None = None
    price: Decimal | None = Field(..., description="in rubles")

    address: str | None = None
    lat: float | None = None
    lng: float | None = None

    time_distance: TimeDistance | None = None

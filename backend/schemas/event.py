import uuid
from decimal import Decimal
from enum import StrEnum

from pydantic import Field
from schemas.base import CamelizedBaseModel


class EventType(StrEnum):
    RESTAURANT = "RESTAURANT"
    EVENT = "EVENT"
    WALK = "WALK"


class Event(CamelizedBaseModel):
    id_: uuid.UUID = Field(..., alias="id")
    type_: EventType = Field(..., alias="type")
    restaurant_type: list[str] | None = None
    name: str | None = None
    description: str | None = None
    link: str | None = None
    img_link: str | None = None
    price: Decimal | None = Field(..., description="in rubles")

    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    reviews: list[str] | None = None

    time: int | None = Field(None, description="in seconds")
    distance: float | None = Field(None, description="in KM")


example_events = [
    Event(
        id=uuid.UUID("018eb4f1-1521-35d6-f1a1-61b57aff2afc"),
        type=EventType.EVENT,
        name="Музей педальных машин",
        description="Современный музей на территории Измайловского кремля расскажет историю педального транспорта и советского автопрома. В экспозиции представлены машины, тракторы, электромобили — всего около 300 экспонатов, а также уникальный архив чертежей и игрушки времен СССР. Для юных посетителей создана мини-трасса, где можно прокатиться на популярных моделях детской техники прошлого. Маленькие автолюбители смогут сдать экзамен по вождению и получить свои первые водительские права.",
        link="https://russpass.ru/event/637d30ff810482a5a109ed6a",
        img_link=None,
        price=Decimal(600),
        address=None,
        lat=None,
        lng=None,
        time=None,
        distance=None,
    )
] * 6


class Events(CamelizedBaseModel):
    events: list[Event]


class Route(CamelizedBaseModel):
    events: list[Event]
    time: int | None = Field(None, description="in seconds")
    distance: float | None = Field(None, description="in KM")

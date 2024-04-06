import uuid
from decimal import Decimal

from schemas.event import Event, EventType

events = [
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
        time_distance=None,
    )
] * 6

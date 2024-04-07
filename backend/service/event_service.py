import random
from dataclasses import dataclass

from repository.pg_repository import PgRepository
from schemas.event import Events


@dataclass
class EventService:
    pg_repository: PgRepository

    def get_events(self) -> Events:
        return self.pg_repository.get_events()

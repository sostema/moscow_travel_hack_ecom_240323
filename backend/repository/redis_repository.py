from dataclasses import dataclass

import redis.asyncio as redis
from shared.settings import app_settings


@dataclass
class RedisRepository:
    def __post_init__(self) -> None:
        self.r = redis.Redis(host=app_settings.redis.host, port=app_settings.redis.port)

    async def health(self) -> None:
        if not await self.r.ping():
            raise Exception("non true ping")

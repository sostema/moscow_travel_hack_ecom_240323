from dataclasses import dataclass

from shared.settings import app_settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@dataclass
class PgRepository:
    def __post_init__(self) -> None:
        self._engine = create_async_engine(
            f"postgresql+asyncpg://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}",
        )

    async def health(self) -> None:
        async with self._engine.connect() as session:
            result = await session.execute(text("select 1"))
            one = result.fetchone()
            if one is not None and one[0] != 1:
                raise Exception('Should be 1 from "select 1"')

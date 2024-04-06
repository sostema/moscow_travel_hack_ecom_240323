import multiprocessing as mp

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSettings(BaseModel):
    host: str = "localhost"
    port: int = 8000
    workers: int = mp.cpu_count() * 2
    log_level: str = "WARNING"
    ssl: bool = False
    ssl_keyfile: str | None = None
    ssl_certfile: str | None = None


class PgSettings(BaseModel):
    database: str = "db_main"
    host: str = "localhost"
    port: int = 5432
    username: str = "db_main"
    password: str = "db_main"


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379


class GigaChatSettings(BaseSettings):
    client_secret: str
    auth_key: str
    client_id: str
    scope: str

    model_config = SettingsConfigDict(
        env_prefix="gigachat_", env_file="/root/.env", env_nested_delimiter="__"
    )


class AppSettings(BaseSettings):
    uvicorn: UvicornSettings = UvicornSettings()
    pg: PgSettings = PgSettings()
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(
        env_prefix="_", env_file=".env", env_nested_delimiter="__"
    )


app_settings = AppSettings()

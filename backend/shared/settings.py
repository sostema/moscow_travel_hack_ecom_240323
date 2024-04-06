import multiprocessing as mp

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    pg_database: str = "db_main"
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "db_main"
    pg_password: str = "db_main"

    redis_host: str = "localhost"
    redis_port: int = 6379

    uvicorn_host: str = "localhost"
    uvicorn_port: int = 8000
    uvicorn_workers: int = mp.cpu_count()
    uvicorn_log_level: str = "WARNING"
    uvicorn_ssl: bool = False
    uvicorn_ssl_keyfile: str | None = None
    uvicorn_ssl_certfile: str | None = None

    gigachat_client_secret: str
    gigachat_auth_key: str
    gigachat_client_id: str
    gigachat_scope: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="_")


app_settings = AppSettings()

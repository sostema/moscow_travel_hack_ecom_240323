from pydantic_settings import BaseSettings, SettingsConfigDict


class GigaChatSettings(BaseSettings):
    client_secret: str
    auth_key: str
    client_id: str
    scope: str

    model_config = SettingsConfigDict(
        extra="allow",
        env_prefix="gigachat_",
        env_file="/root/.env",
        env_nested_delimiter="__",
    )


class PGVectorSettings(BaseSettings):
    host: str
    pwd: str
    connection_name: str

    model_config = SettingsConfigDict(
        extra="allow",
        env_prefix="pg_",
        env_file="/root/.env",
        env_nested_delimiter="__",
    )


gigachat_settings = GigaChatSettings()
pgvector_settings = PGVectorSettings()

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class GigaChatSettings(BaseSettings):
#     client_secret: str
#     auth_key: str
#     client_id: str
#     scope: str

#     model_config = SettingsConfigDict(
#         extra="allow",
#         env_prefix="gigachat_",
#         env_file="/root/.env",
#         env_nested_delimiter="__",
#     )


# class PGVectorSettings(BaseSettings):
#     host: str
#     pwd: str

#     model_config = SettingsConfigDict(
#         extra="allow",
#         env_prefix="pg_",
#         env_file="/root/.env",
#         env_nested_delimiter="__",
#     )


# gigachat_settings = GigaChatSettings()
# pgvector_settings = PGVectorSettings()

# pgvector_connection_string = f"postgresql+psycopg2://db_main:{pgvector_settings.pwd}@{pgvector_settings.host}:5432/db_main"

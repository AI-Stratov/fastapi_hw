from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "TODO APP"
    API_V1_STR: str = "/api/v1"
    APP_CORS_ALLOW_ORIGINS: list[str]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


app_settings = AppSettings()  # type: ignore


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


auth_settings = AuthSettings()  # type: ignore


class DatabaseSettings(BaseSettings):
    DB_SCHEMA: str
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT_SEC: int = 30
    DB_POOL_RECYCLE_SEC: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


db_settings = DatabaseSettings()  # type: ignore

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NOTIFYSTACK_", extra="ignore")

    app_name: str = "NotifyStack OSS"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./notifystack.db"
    jwt_secret: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_exp_minutes: int = 10080


settings = Settings()

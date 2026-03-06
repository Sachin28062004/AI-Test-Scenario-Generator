from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    grok_api_key: str = ""
    encryption_key: str = ""
    jwt_secret: str = "change-me-in-production-use-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"


settings = Settings()

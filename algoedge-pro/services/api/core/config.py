from __future__ import annotations
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "sqlite:///./db.sqlite3"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev"
    allowed_origins: List[str] = ["*"]

    class Config:
        env_prefix = ""
        env_file = ".env"


settings = Settings()
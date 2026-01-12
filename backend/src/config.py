from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./todo_app.db"  # Use SQLite for development/testing

    # Auth settings
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
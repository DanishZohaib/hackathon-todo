from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./todo_app.db"  # Use SQLite for development/testing

    # Auth settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://172.22.240.1:3000", "http://172.22.240.1:*"]

    # Environment
    ENVIRONMENT: str = "development"

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v):
        if not v or len(v) == 0:
            raise ValueError('SECRET_KEY must be set in environment variables')
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long for security')
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
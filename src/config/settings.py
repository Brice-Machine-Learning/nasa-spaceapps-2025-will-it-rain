import os
from functools import lru_cache
from pydantic_settings import BaseSettings

"""src/config/settings.py"""

"""
Project settings for FastAPI app.
Centralizes configuration with environment variable support.
"""


class Settings(BaseSettings):
    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: str = "NASA Space Apps – Will It Rain"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
    ENV: str = os.environ.get("ENV", "development")  # development | production | test

    # -------------------------------------------------------------------------
    # API Keys / External Services
    # -------------------------------------------------------------------------
    OPENWEATHER_API_KEY: str | None = None  # optional, loaded from .env
    NASA_API_KEY: str | None = None

    # -------------------------------------------------------------------------
    # Database (if needed later)
    # -------------------------------------------------------------------------
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

    # -------------------------------------------------------------------------
    # Security (expand if you add auth later)
    # -------------------------------------------------------------------------
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    # -------------------------------------------------------------------------
    # Paths
    # -------------------------------------------------------------------------
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Cached settings (singleton)
@lru_cache()
def get_settings() -> Settings:
    return Settings()

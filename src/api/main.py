"""src/api/main.py"""

from fastapi import FastAPI
from src.config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)





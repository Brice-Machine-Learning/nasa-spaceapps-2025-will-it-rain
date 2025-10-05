"""src/api/routes/health.py"""
from fastapi import APIRouter
from src.config.settings import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "debug": settings.DEBUG,
        "environment": settings.ENV,
    }

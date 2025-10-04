"""src/api/routes/location.py"""

from fastapi import APIRouter
from src.config.settings import get_settings

router = APIRouter()
settings = get_settings()

@router.get('/location')
def get_location():
    return {
        "latitude": settings.LOCATION_LATITUDE,
        "longitude": settings.LOCATION_LONGITUDE,
    }

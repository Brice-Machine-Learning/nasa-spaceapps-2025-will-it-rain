"""src/services/location_service.py"""

import httpx
from functools import lru_cache
from src.config.settings import get_settings

settings = get_settings()

BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"


@lru_cache(maxsize=128)
def _cached_call(query: str, limit: int):
    """Internal helper cached by query string."""
    params = {"q": query, "limit": limit, "appid": settings.OPENWEATHER_API_KEY}
    response = httpx.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


async def fetch_coordinates(city: str, state: str = None, country: str = "US", limit: int = 1):
    """Fetch coordinates with in-memory caching."""
    query = f"{city},{state},{country}" if state else f"{city},{country}"
    data = _cached_call(query, limit)

    if not data:
        return {"error": "Location not found"}

    result = data[0]
    return {
        "city": result.get("name"),
        "state": state,
        "country": result.get("country"),
        "latitude": result.get("lat"),
        "longitude": result.get("lon"),
        "cached": True,
    }


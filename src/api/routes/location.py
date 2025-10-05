"""src/api/routes/location.py"""

from fastapi import APIRouter, HTTPException
from src.services.location_service import fetch_coordinates   # ✅ correct for a module layout

router = APIRouter(prefix="/location", tags=["Location"])

@router.get("/{city}")
async def get_location(city: str, state: str = None, country: str = "US"):
    result = await fetch_coordinates(city, state, country)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


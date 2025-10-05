from fastapi import APIRouter, HTTPException
from src.services.dataset_service import fetch_nasa_power_data

""" 
src/api/routes/dataset.py 

API route to fetch datasets from NASA POWER API.
"""

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.get("/{lat}/{lon}")
async def get_dataset(lat: float, lon: float):
    """Fetch daily weather data from NASA POWER."""
    try:
        summary, _ = await fetch_nasa_power_data(lat, lon)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

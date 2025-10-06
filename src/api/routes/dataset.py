from fastapi import APIRouter, HTTPException, Query
from src.services.dataset_service import fetch_nasa_power_data

""" 
src/api/routes/dataset.py
API route to fetch datasets from NASA POWER API.
"""

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.get("/{lat}/{lon}")
async def get_dataset(
    lat: float,
    lon: float,
    start: str = Query(None, description="Start date in YYYYMMDD format"),
    end: str = Query(None, description="End date in YYYYMMDD format"),
):
    """Fetch NASA POWER daily dataset for a given coordinate and date range."""
    try:
        summary, _ = await fetch_nasa_power_data(lat, lon, start=start, end=end)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


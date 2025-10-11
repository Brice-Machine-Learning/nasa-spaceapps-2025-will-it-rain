from fastapi import APIRouter, HTTPException, Query
from src.services.location_service import fetch_coordinates
from src.services.dataset_service import fetch_nasa_power_data

"""
src/api/routes/dataset.py
API route to fetch NASA POWER dataset for a given city and return it as a CSV download.
"""

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.get("")
async def get_dataset_by_city(
    city: str = Query(..., description="City name, e.g., 'Orlando'"),
    state: str = Query(None, description="State code, e.g., 'FL'"),
    country: str = Query("US", description="Country code, e.g., 'US'"),
    start: str = Query(None, description="Start date in YYYYMMDD format"),
    end: str = Query(None, description="End date in YYYYMMDD format"),
):
    """
    Fetch NASA POWER dataset for a given city and store it internally.
    Returns metadata (not a file download) for ML pipeline use.
    """
    try:
        # Step 1: Resolve coordinates
        location = await fetch_coordinates(city=city, state=state, country=country)
        if not location or "latitude" not in location:
            raise HTTPException(status_code=404, detail=f"Coordinates not found for '{city}, {state or ''}'")

        lat, lon = location["latitude"], location["longitude"]

        # Step 2: Fetch dataset (or load cached)
        meta, _ = await fetch_nasa_power_data(lat, lon, start=start, end=end)

        # Step 3: Return JSON summary for downstream ML
        return {
            "city": location["city"],
            "state": location.get("state"),
            "latitude": lat,
            "longitude": lon,
            "dataset": meta["dataset"],
            "rows": meta["rows"],
            "columns": meta["columns"],
            "file_path": meta["file_path"],
            "status": meta["status"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

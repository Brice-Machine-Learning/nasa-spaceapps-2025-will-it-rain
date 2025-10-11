import pytest
import httpx
from src.api.main import app

"""tests/test_dataset_routes.py

Unit tests for FastAPI endpoints using httpx.AsyncClient (v0.28+).
"""


@pytest.mark.asyncio
async def test_dataset_endpoint_success(monkeypatch, tmp_path):
    """Mock NASA and OpenWeather services to test /dataset endpoint end-to-end without network calls."""
    from src.api.routes import dataset

    # --- Mock fetch_coordinates (OpenWeather) ---
    async def mock_fetch_coordinates(city, state=None, country="US", limit=1):
        return {
            "city": city,
            "state": state,
            "country": country,
            "latitude": 28.5383,
            "longitude": -81.3792,
            "cached": True,
        }

    # --- Mock fetch_nasa_power_data (NASA POWER) ---
    async def mock_fetch_nasa_power_data(lat, lon, start=None, end=None):
        fake_csv = tmp_path / f"nasa_power_{lat}_{lon}.csv"
        fake_csv.write_text("YEAR,MO,DY,T2M\n2025,10,10,25.0\n")
        meta = {
            "dataset": "NASA POWER",
            "lat": lat,
            "lon": lon,
            "start": start or "20250101",
            "end": end or "20251010",
            "rows": 1,
            "columns": ["YEAR", "MO", "DY", "T2M"],
            "file_path": str(fake_csv),
            "status": "mocked success"
        }
        return meta, None

    monkeypatch.setattr(dataset, "fetch_coordinates", mock_fetch_coordinates)
    monkeypatch.setattr(dataset, "fetch_nasa_power_data", mock_fetch_nasa_power_data)

    # --- Call endpoint ---
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/dataset?city=Orlando&state=FL&start=20250101&end=20250105")

    # --- Assertions ---
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Orlando"
    assert data["dataset"] == "NASA POWER"
    assert "file_path" in data
    assert data["status"] == "mocked success"

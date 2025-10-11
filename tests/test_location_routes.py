import pytest
import httpx
from src.api.main import app

"""tests/test_location_routes.py

Unit tests for FastAPI endpoints using httpx.AsyncClient (v0.28+).
"""


@pytest.mark.asyncio
async def test_location_endpoint_success(monkeypatch):
    """Mock fetch_coordinates to test /location/{city} without hitting API."""
    from src.api.routes import location

    async def mock_fetch(city, state=None, country="US", limit=1):
        return {
            "city": city,
            "state": state,
            "country": country,
            "latitude": 39.7392,
            "longitude": -104.9903,
            "cached": False,
        }

    monkeypatch.setattr(location, "fetch_coordinates", mock_fetch)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/location/Denver?state=CO")

    assert response.status_code == 200
    result = response.json()
    assert result["city"] == "Denver"
    assert pytest.approx(result["latitude"], rel=1e-3) == 39.7392
    assert "cached" in result


@pytest.mark.asyncio
async def test_location_not_found(monkeypatch):
    """Simulate a not-found error response."""
    from src.api.routes import location

    async def mock_fetch(city, state=None, country="US", limit=1):
        return {"error": "Location not found"}

    monkeypatch.setattr(location, "fetch_coordinates", mock_fetch)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/location/UnknownCity")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Location not found"

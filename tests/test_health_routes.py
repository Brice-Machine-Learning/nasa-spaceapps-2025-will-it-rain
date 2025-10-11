import pytest
import httpx
from src.api.main import app

"""tests/test_health_routes.py

Unit tests for FastAPI endpoints using httpx.AsyncClient (v0.28+).
"""


@pytest.mark.asyncio
async def test_health_endpoint():
    """Ensure /health returns expected status."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"

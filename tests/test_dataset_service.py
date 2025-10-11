"""
Test suite for DatasetService class.
tests/test_dataset_service.py
"""

import os
import pytest
import pandas as pd
from src.services.dataset_service import fetch_nasa_power_data

@pytest.mark.asyncio
async def test_fetch_nasa_power_data(tmp_path):
    """
    Integration test for the NASA POWER dataset fetcher.
    - Verifies API call succeeds for a known coordinate
    - Ensures a CSV file is written to disk
    - Checks expected columns exist
    - Confirms caching works on subsequent calls
    """

    # Use a small test window to avoid long downloads
    lat, lon = 28.5383, -81.3792  # Orlando, FL
    start, end = "20250101", "20250105"

    # Temporarily override data directory for isolation
    data_dir = tmp_path / "raw"
    os.makedirs(data_dir, exist_ok=True)
    os.chdir(tmp_path)  # ensures DATA_DIR resolves locally

    meta, df = await fetch_nasa_power_data(lat, lon, start, end)

    # --- Assertions ---
    assert isinstance(meta, dict)
    assert isinstance(df, pd.DataFrame)
    assert meta["dataset"] == "NASA POWER"
    assert "YEAR" in df.columns
    assert "T2M" in df.columns
    assert len(df) > 0
    assert os.path.exists(meta["file_path"])

    # Call again → should return cached
    meta_cached, df_cached = await fetch_nasa_power_data(lat, lon, start, end)
    assert "cached" in meta_cached["status"]
    assert meta_cached["file_path"] == meta["file_path"]
    assert df_cached.equals(df)

import httpx
import pandas as pd
from io import StringIO
from datetime import date

"""
src/services/dataset_service.py

Service to fetch and preprocess datasets from NASA POWER API.
"""

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

async def fetch_nasa_power_data(lat: float, lon: float, start: str = None, end: str = None):
    """
    Fetch daily weather data from NASA POWER API in CSV format
    for given coordinates and date range.
    """

    # Default to current year if not specified
    year = date.today().year
    start = start or f"{year}0101"
    end = end or f"{year}1231"

    params = {
        "parameters": "PRECTOT,T2M,RH2M",  # Precipitation, Temp, Humidity
        "start": start,
        "end": end,
        "latitude": lat,
        "longitude": lon,
        "format": "CSV",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        csv_data = response.text

    # Parse CSV into DataFrame
    df = pd.read_csv(StringIO(csv_data), skiprows=10)  # Skip NASA metadata rows
    df = df.dropna(how="all").reset_index(drop=True)

    # Optional: Keep only relevant columns
    expected_cols = ["YEAR", "MO", "DY", "PRECTOT", "T2M", "RH2M"]
    df = df[[c for c in df.columns if c in expected_cols]]

    # Return JSON summary for API or DataFrame for preprocessing
    return {
        "dataset": "NASA POWER",
        "lat": lat,
        "lon": lon,
        "rows": len(df),
        "columns": list(df.columns),
        "status": "downloaded"
    }, df

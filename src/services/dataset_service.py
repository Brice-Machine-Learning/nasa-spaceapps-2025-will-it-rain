import os
import httpx
import pandas as pd
from io import StringIO
from datetime import datetime

""" 
src/services/dataset_service.py
Service to fetch and cache datasets from NASA POWER API.
"""

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
DATA_DIR = os.path.join(os.getcwd(), "data", "raw")

os.makedirs(DATA_DIR, exist_ok=True)


# def parse_nasa_csv(csv_text: str) -> pd.DataFrame:
#     """
#     Parse NASA POWER CSV dynamically by skipping everything up to '-END HEADER-'.
#     Works across all POWER products and date ranges.
#     """
#     lines = csv_text.splitlines()

#     # find the end of the metadata header
#     end_header_idx = None
#     for i, line in enumerate(lines):
#         if line.strip().startswith("-END HEADER-"):
#             end_header_idx = i
#             break

#     if end_header_idx is None:
#         raise ValueError("Could not find '-END HEADER-' in NASA CSV text")

#     # everything after that line is the actual CSV table
#     csv_data = "\n".join(lines[end_header_idx + 1 :]).strip()

#     if not csv_data or "YEAR" not in csv_data:
#         raise ValueError("NASA CSV body found, but no YEAR column — possible format mismatch")

#     df = pd.read_csv(StringIO(csv_data))
#     df = df.dropna(how="all").reset_index(drop=True)
#     print(f"✅ Parsed {len(df)} rows, {len(df.columns)} columns from NASA POWER CSV")
#     return df




async def fetch_nasa_power_data(lat: float, lon: float, start: str = None, end: str = None):
    """
    Fetch daily weather data from NASA POWER API for given coordinates and date range.
    Automatically splits long ranges into yearly chunks to avoid 422 errors.
    Caches combined CSV in /data/raw/.
    """

    # Default: one year ending today
    today = datetime.utcnow()
    if not start:
        start = f"{today.year - 1}0101"
    if not end:
        end = f"{today.year}{today.month:02d}{today.day:02d}"

    # Construct file path for combined dataset
    filename = f"nasa_power_{lat:.4f}_{lon:.4f}_{start}_{end}.csv"
    file_path = os.path.join(DATA_DIR, filename)

    # ✅ Return cached file if available
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return {
            "dataset": "NASA POWER",
            "lat": lat,
            "lon": lon,
            "start": start,
            "end": end,
            "rows": len(df),
            "columns": list(df.columns),
            "file_path": file_path,
            "status": "cached (existing file used)"
        }, df

    # Prepare chunked date ranges by year
    start_year = int(start[:4])
    end_year = int(end[:4])
    dfs = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for year in range(start_year, end_year + 1):
            chunk_start = f"{year}0101"
            chunk_end = f"{year}1231"

            params = {
                "parameters": "PRECTOTCORR,T2M,RH2M",
                "start": chunk_start,
                "end": chunk_end,
                "latitude": lat,
                "longitude": lon,
                "community": "AG",
                "format": "CSV",
            }

            try:
                response = await client.get(BASE_URL, params=params)
                # ========================================
                print("🔍 STATUS:", response.status_code)
                print("🔍 HEADERS:", response.headers)
                print("🔍 RAW TEXT PREVIEW:", response.text[:300])
                # ========================================
                response.raise_for_status()
                df_chunk = pd.read_csv(StringIO(response.text), skiprows=10)
                df_chunk = df_chunk.dropna(how="all").reset_index(drop=True)
                dfs.append(df_chunk)
                print(f"✅ Downloaded {year} for ({lat}, {lon})")
            except httpx.HTTPStatusError as e:
                print(f"⚠️ Skipping {year} due to error: {e}")
                continue

    if not dfs:
        raise ValueError(f"No valid data fetched for {lat}, {lon} in range {start}–{end}")

    # Combine yearly chunks
    df = pd.concat(dfs, ignore_index=True)
    expected_cols = ["YEAR", "MO", "DY", "PRECTOT", "T2M", "RH2M"]
    df = df[[c for c in df.columns if c in expected_cols]]

    # Save combined CSV
    df.to_csv(file_path, index=False)

    return {
        "dataset": "NASA POWER",
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end,
        "rows": len(df),
        "columns": list(df.columns),
        "file_path": file_path,
        "status": f"downloaded ({start_year}–{end_year}) and saved"
    }, df


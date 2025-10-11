# scripts/manual_dataset_download.py

"""
This script demonstrates how to manually download NASA POWER dataset for a specific location and time period. It utilizes the `fetch_nasa_power_data` function from the `src.services.dataset_service` module to retrieve the data asynchronously.
"""

import asyncio
from src.services.dataset_service import fetch_nasa_power_data

async def main():
    # Example: Orlando, FL
    lat, lon = 28.5383, -81.3792
    start, end = "20250101", "20250110"

    meta, df = await fetch_nasa_power_data(lat, lon, start, end)

    print("\n✅ DOWNLOAD COMPLETE")
    print(f"File path: {meta['file_path']}")
    print(f"Rows: {meta['rows']}, Columns: {meta['columns']}")
    print("\n📊 DataFrame preview:")
    print(df.head())

if __name__ == "__main__":
    asyncio.run(main())

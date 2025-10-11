import httpx
from io import StringIO
import pandas as pd

url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "PRECTOTCORR,T2M,RH2M",
    "start": "20240101",
    "end": "20240930",
    "latitude": 39.7392,
    "longitude": -104.9903,
    "community": "AG",
    "format": "CSV"
}

r = httpx.get(url, params=params)
df = pd.read_csv(StringIO(r.text), skiprows=10)
print(df.head())

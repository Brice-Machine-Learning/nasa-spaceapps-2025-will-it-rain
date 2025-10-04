# 🌍 API Route Map – NASA Space Apps 2025

## 1. Health Check

- **Route**: `GET /health`  
- **Purpose**: Verify service is alive.  
- **Response**:  

```json
{ "status": "ok", "debug": true, "environment": "development" }
```

---

## 2. Location → Lat/Long Lookup

- **Route**: `GET /location/{city_name}`  
- **Purpose**: Convert `"Denver, CO"` into lat/long (via NASA/NOAA or OpenWeather geocoding).  
- **Response**:  

```json
{
  "city": "Denver",
  "state": "CO",
  "latitude": 39.7392,
  "longitude": -104.9903
}
```

---

## 3. Fetch Dataset for Location

- **Route**: `GET /dataset/{lat}/{lon}`  
- **Purpose**: Download NASA climate/precip dataset (CSV or JSON).  
- **Response**:  

```json
{
  "dataset": "NASA Power",
  "lat": 39.7392,
  "lon": -104.9903,
  "rows": 365,
  "file": "data/raw/denver_weather.csv"
}
```

---

## 4. Preprocess Dataset

- **Route**: `POST /preprocess`  
- **Purpose**: Clean and feature-engineer dataset for ML.  
- **Request**: dataset name/file id.  
- **Response**: processed schema summary.  

---

## 5. Run Prediction

- **Route**: `POST /predict`  
- **Purpose**: Run ML model on preprocessed dataset for a date.  
- **Request**:  

```json
{
  "location": "Denver, CO",
  "date": "2025-10-06"
}
```

- **Response**:  

```json
{
  "rain_probability": 0.72,
  "confidence": 0.85,
  "features": { "temp": 21.1, "humidity": 64 }
}
```

---

## 6. Visualization (Stretch Goal)

- **Route**: `GET /visualize/{location}`  
- **Purpose**: Return a chart showing rain probabilities over time.  

---

## ⚙️ Workflow (End-to-End)

1. User hits `/predict` with `location="Denver, CO"` + date.  
2. API calls **location service** → returns lat/long.  
3. API calls **dataset service** → fetches NASA data → saves CSV.  
4. **Preprocess pipeline** cleans data → extracts features.  
5. **ML model** runs prediction → outputs probability + confidence.  
6. Response returned to user.  

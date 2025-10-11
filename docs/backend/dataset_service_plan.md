# 🌎 Dataset Service Plan

## NASA Space Apps 2025 – *“Will It Rain?”*

## Component: Backend Dataset Retrieval Layer

---

## 🧩 Purpose

The **Dataset Service** will act as the bridge between the backend’s `/location` route and the machine-learning model input pipeline.  
It enables the system to automatically fetch, parse, and prepare climate data from NASA’s public datasets — specifically the **NASA POWER Project**, which supports programmatic CSV downloads based on latitude and longitude coordinates.

This component eliminates the need for manual data downloads while keeping the workflow fully automated and reproducible.

---

## 🧠 Design Philosophy

- **Automated**: Allow the backend to dynamically fetch CSVs based on user location.
- **Stateless**: Each request is independent; caching may be added later.
- **Transparent**: Use open NASA POWER endpoints (no API keys).
- **Extensible**: Can later be swapped for other data sources (e.g., NOAA GHCN) without affecting the API layer.

---

## ⚙️ Functional Overview

| Step | Description | Output |
|------|--------------|--------|
| **1. Input** | Receives latitude and longitude from `/location` response or directly from the frontend. | `(lat: float, lon: float)` |
| **2. URL Construction** | Builds NASA POWER CSV URL using query parameters for precipitation, temperature, and humidity across a default or user-specified date range. | NASA download URL (string) |
| **3. Data Retrieval** | Makes HTTP GET request using `httpx` to fetch the CSV from NASA’s servers. | Raw CSV text |
| **4. Parsing** | Reads CSV into a Pandas DataFrame using `StringIO`. | DataFrame |
| **5. Validation** | Checks for expected columns (`PRECTOT`, `T2M`, `RH2M`, etc.) and ensures non-empty dataset. | Cleaned DataFrame |
| **6. Output** | Returns either: (a) summary JSON for API response, or (b) DataFrame for downstream preprocessing. | `{ "rows": int, "columns": list, "status": "success" }` |

---

## 📦 File Location

- `src/services/dataset_service.py` – Main service logic.

---

## 🧰 Responsibilities

1. **Construct NASA POWER URL**  
   - Parameters: latitude, longitude, start_date, end_date  
   - Example template:  

     ```text
     https://power.larc.nasa.gov/api/temporal/daily/point
       ?parameters=PRECTOT,T2M,RH2M
       &start={YYYYMMDD}
       &end={YYYYMMDD}
       &latitude={lat}
       &longitude={lon}
       &format=CSV
     ```

2. **Perform Data Fetch**  
   - Use `httpx.AsyncClient` to request the CSV.  
   - Raise clear HTTP exceptions for timeout or connection issues.  
   - Log request duration and NASA response code.

3. **Parse and Clean CSV**  
   - Load CSV using Pandas.  
   - Drop empty rows or irrelevant metadata sections.  
   - Normalize column names for consistent downstream processing.

4. **Summarize Output**  
   - Return JSON summary (rows, columns, time range).  
   - Optionally, persist the CSV temporarily in `data/raw/`.

---

## 📤 Expected Input / Output

### Input Example

```json
{
  "latitude": 39.7392,
  "longitude": -104.9903,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

---

### Output Example

```json
{
  "dataset": "NASA POWER",
  "lat": 39.7392,
  "lon": -104.9903,
  "rows": 365,
  "columns": ["YEAR", "MO", "DY", "PRECTOT", "T2M", "RH2M"],
  "status": "downloaded"
}
```

---

## 🧩 Integration Points

| Component | Interaction |
|------------|--------------|
| **`/location` Route** | Supplies latitude and longitude from user input to trigger dataset retrieval. |
| **`/dataset` Route** | Exposes the dataset retrieval service as a public API endpoint for the frontend and integration testing. |
| **`/preprocess` Service** | Consumes the parsed DataFrame to perform feature engineering and cleaning before model input. |
| **`/predict` Endpoint** | Accesses processed features from the preprocessing step to run the ML inference pipeline. |
| **Local Data Layer (`data/raw/`)** | Optionally stores fetched CSVs for debugging, offline testing, or fallback when NASA service is unavailable. |

---

## 🧠 Future Enhancements

| Feature | Description | Benefit |
|----------|--------------|----------|
| **Redis Caching** | Cache datasets by `(lat, lon, date range)` to minimize redundant NASA downloads and reduce network overhead. | Faster repeat queries; reduced NASA server load. |
| **Fallback to Local Data** | Automatically load a cached or bundled CSV from `data/raw/` if the NASA request fails. | Ensures offline reliability during hackathon demo. |
| **Date Range Selection** | Allow users or the frontend to specify a custom start and end date. | Improves flexibility and temporal control for model input. |
| **Expanded Parameter Set** | Add additional features such as cloud cover, wind speed, and solar irradiance to enhance predictive accuracy. | Enriches model performance and contextual insights. |
| **Error Logging & Retries** | Implement structured logging with automatic retry on failed NASA requests. | Increases robustness and traceability. |
| **CSV Storage Policy** | Define rules for temporary vs. permanent CSV retention (e.g., auto-delete after 24 hours). | Reduces local storage footprint. |

---

## ✅ Success Criteria

| Criterion | Target |
|------------|---------|
| **Automated Retrieval** | The backend successfully builds and fetches NASA POWER CSVs using dynamic lat/lon inputs. |
| **Data Integrity** | Retrieved CSVs contain non-empty, valid numerical fields for precipitation, temperature, and humidity. |
| **Schema Consistency** | The returned DataFrame or JSON summary conforms to a predefined schema expected by the preprocessing module. |
| **Error Handling** | NASA unavailability or invalid coordinates produce clear, informative error messages (not crashes). |
| **Integration Ready** | `/dataset` output is immediately consumable by `/preprocess` without manual transformation. |

---

## 🧾 Testing & Validation Strategy

1. **Unit Tests (Offline)**  
   - Mock NASA POWER CSV responses with local test files under `tests/data/`.  
   - Validate parsing, column names, and row count.  

2. **Integration Tests (Online)**  
   - Test live CSV downloads for 2–3 known coordinates (e.g., Denver, FL, Mumbai).  
   - Assert that data structure and response time meet baseline performance thresholds.  

3. **Failure Tests**  
   - Simulate invalid coordinates or NASA downtime.  
   - Confirm error responses are handled gracefully and logged.  

---

## 🧩 Deliverables Summary

| Deliverable | Description | Status |
|--------------|--------------|--------|
| **`dataset_service.py`** | Service module handling URL construction, download, and parsing. | 🚧 In Progress |
| **`/dataset` Route** | API layer wrapping the service for frontend or model access. | 🚧 Planned |
| **Unit Tests (`test_dataset_service.py`)** | Covers valid fetch, invalid city, and caching behavior. | ☐ Pending |
| **Documentation** | Completed design plan (this file). | ✅ Complete |

---

## 💡 Summary

The **Dataset Service** will transform user-provided locations into actionable weather data pulled directly from NASA’s POWER system.  
By automating CSV retrieval and standardizing data formatting, this service becomes the backbone of the data pipeline, bridging geolocation, preprocessing, and prediction.  

Once implemented, it ensures the backend can deliver clean, feature-rich inputs to the ML model, enabling accurate and efficient rainfall probability predictions.

---

**Prepared by:**  
**Brice Nelson**  
*Backend & Infrastructure Lead – NASA Space Apps 2025 “Will It Rain?”*  

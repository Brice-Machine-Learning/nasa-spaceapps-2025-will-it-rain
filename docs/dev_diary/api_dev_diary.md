---
title: "API Development Diary – NASA POWER Integration"
date: 2025-10-05
author: Brice Nelson
role: Backend & Infrastructure Lead
project: NASA Space Apps 2025 – "Will It Rain?"
---

# API Development Diary – NASA POWER Integration
**Date:** October 05, 2025  
**Author:** Brice Nelson  
**Role:** Backend & Infrastructure Lead  
**Project:** NASA Space Apps 2025 – “Will It Rain?”  

---

## 🧩 Overview  

The backend API forms the foundation of our project’s architecture. Its purpose is to serve as the central point of communication between the user interface, external weather/geospatial APIs, and the machine-learning model responsible for predicting weather conditions.  

Over the past development cycle, the backend has evolved from a placeholder FastAPI scaffold into a functional, modular service capable of fetching and validating live geospatial data. The focus to date has been on **establishing a reliable, testable, and extensible framework** that the rest of the system can build upon during model and data integration.

---

## ✅ Work Completed to Date  

### 1. **FastAPI Backend Established**

- Set up a production-ready FastAPI application with full modular routing (`/health`, `/location`).
- Added metadata, CORS configuration, and a consistent settings pattern to ensure compatibility across local and integration environments.  
- Integrated Pydantic-based configuration management via `settings.py` for environment variables and API credentials.  

### 2. **Location Service Implementation**

- Built a dedicated service layer (`location_service.py`) responsible for converting city and state names into geographic coordinates (latitude and longitude).
- Integrated the **OpenWeather Geocoding API** to ensure accurate and globally consistent location lookups.
- Implemented **in-memory caching** (`lru_cache`) to avoid repeated API calls and improve response performance—important for hackathon time constraints and potential rate limits.
- Added graceful error handling to return structured JSON error messages when invalid or unknown cities are requested.

### 3. **Routing and Endpoint Design**

- Developed a fully functional `/location/{city}` route that communicates with the location service and provides formatted JSON responses.  
- Standardized API response shapes to prepare for downstream integration with NASA/NOAA datasets and the ML prediction endpoint.  
- Created a `/health` route to support CI/CD, container readiness checks, and basic API uptime verification.  

### 4. **Automated Testing Framework**

- Established a comprehensive **pytest** environment with `pytest-asyncio` for async route testing.
- Configured tests to run entirely offline by mocking API calls, ensuring that functionality can be validated without internet access or external dependencies.
- Updated all tests to be compatible with modern `httpx` versions using the new `ASGITransport` interface.
- All tests now **pass successfully**, confirming that the backend routes, async logic, and error handling perform as expected.

### 5. **Branching and CI Alignment**

- Confirmed alignment with the repository’s branching strategy defined in `contributing.md`:  
  `backend-api` (Brice) merges into `integration` for model linkage and full-pipeline validation.  
- GitHub Actions CI/CD workflow configured to run linting and tests automatically on push and PR.

---

## 🧠 Why These Steps Matter  

These milestones represent the **foundational plumbing** required before connecting to datasets or models.

- The **FastAPI structure** ensures scalability and maintainability once additional endpoints are added.  
- The **location service** provides the key link between user input (“Denver, CO”) and the geospatial coordinates that NASA/NOAA datasets require.  
- The **testing framework** guarantees that each addition to the backend can be verified quickly during the hackathon, reducing integration risk.  
- **Caching and async design** make the service performant enough for real-time inference without unnecessary API overhead.  

In short: the backend is now **API-ready, tested, and positioned for integration** with the machine-learning model pipeline.

---

## 🔭 Next Steps  

| Priority | Task | Description |
|-----------|-------|-------------|
| **1** | **Dataset Endpoint (`/dataset/{lat}/{lon}`)** | Implement a route to pull NASA or NOAA climate data for the provided coordinates. Output will be stored locally (CSV/JSON) or streamed directly to preprocessing. |
| **2** | **Preprocessing Service (`/preprocess`)** | Add logic for feature cleaning and engineering to standardize the data before it reaches the model. |
| **3** | **Prediction Endpoint (`/predict`)** | Integrate the ML model (from the data branch) to return rainfall probability and confidence metrics for a given location/date. |
| **4** | **Redis or File-based Caching (Stretch Goal)** | Replace in-memory cache with Redis for persistence across sessions and scalability. |
| **5** | **Containerization and Deployment** | Wrap backend into a lightweight Docker container for reproducible deployments and local demos. |
| **6** | **Documentation & Presentation Prep** | Finalize API documentation (OpenAPI/Swagger), add visualizations of pipeline flow, and prepare assets for hackathon presentation. |

---

## 🧭 Current Status Summary  

| Area | Status | Notes |
|------|---------|-------|
| Backend App Structure | ✅ Complete | Modular FastAPI design finalized |
| Location Lookup Endpoint | ✅ Complete | Cached, tested, and validated |
| Testing Framework | ✅ Complete | Full async tests passing |
| Dataset + Model Integration | 🚧 Pending | Next development milestone |
| Caching Layer (Redis) | 🚧 Optional | Enhancement for production |
| Docker / CI | ⚙️ In Progress | Will follow integration testing |

---

## 💡 Key Takeaway  

The backend now provides a **stable, extensible, and verified API layer** that can confidently support the next phase of development — connecting live climate datasets and integrating the predictive model.  
All subsequent endpoints will build on this foundation to deliver the final *“Will It Rain?”* MVP.  

---

## 🧩 Dataset Service Enhancements  

### Context  

As the project transitioned from location-based geocoding to weather dataset retrieval, we encountered limitations in the NASA POWER API.  
Initially, the backend attempted to pull multi-year CSV datasets (e.g., 2015–2024) in a single API call. However, NASA POWER rejects long-range queries with a **422 Unprocessable Entity** error because the server only supports smaller temporal windows.  

To solve this, we re-engineered the `/dataset/{lat}/{lon}` service to:  

1. Automatically **split long date ranges into yearly chunks**,  
2. Retrieve and merge all years into a single consolidated dataset, and  
3. Implement **local caching** to avoid redundant API calls.  

These enhancements now allow the backend to download and store robust, multi-year weather datasets for model training while remaining within NASA’s API constraints.  

---

### Key Improvements  

#### 1. **Chunked Retrieval**  

- Multi-year requests (e.g., 2015–2024) are automatically broken into **year-by-year downloads**.  
- Each year’s CSV is fetched separately and concatenated into a single DataFrame.  
- This prevents API 422 errors while supporting large-scale data assembly for model training.  

#### 2. **Automatic Local Caching**  

- Fetched CSVs are saved to `/data/raw/` using coordinate and date-based filenames:  

  ```text
  nasa_power_<lat>_<lon>_<start>_<end>.csv
  ```

- On subsequent requests for the same coordinates and date range, the backend **skips re-downloading** and serves the existing file instantly.  
- Significantly reduces latency and NASA API load during development and testing.  

#### 3. **Configurable Date Ranges**  

- The route now supports optional query parameters:  

  ```text
  /dataset/{lat}/{lon}?start=YYYYMMDD&end=YYYYMMDD
  ```

- Default range remains the **last 365 days**, but developers can specify multi-year spans for training data collection.  

#### 4. **Resilience and Logging**  

- Failed year-chunks (e.g., missing or incomplete data) are skipped automatically without breaking the pipeline.  
- Console logs and (soon) persistent file-based logs record all dataset fetch events, including cached retrievals.  

---

### Example Request & Response  

**Request:**  

```sql
GET /dataset/39.7392/-104.9903?start=20150101&end=20241231
```

**Response:**  

```json
{
  "dataset": "NASA POWER",
  "lat": 39.7392,
  "lon": -104.9903,
  "start": "20150101",
  "end": "20241231",
  "rows": 3650,
  "columns": ["YEAR", "MO", "DY", "PRECTOT", "T2M", "RH2M"],
  "file_path": "/data/raw/nasa_power_39.7392_-104.9903_20150101_20241231.csv",
  "status": "downloaded (2015–2024) and saved"
}
```

---

### Why This Matters  

| Issue | Solution | Benefit |
|--------|-----------|----------|
| NASA API rejects long date ranges (422) | Automatic year-based chunking | Full multi-year training data now supported |
| Repeated downloads of same dataset | Local file caching | Faster response, reduced bandwidth |
| Manual data assembly for training | Auto-concatenation of yearly CSVs | Single combined dataset ready for ML |
| High API latency for testing | Cache detection & reuse | Instant local fetch after first request |

---

### Architectural Impact  

| Layer | Enhancement | Description |
|--------|--------------|-------------|
| **Service Layer** | `dataset_service.py` rewritten for async chunking, caching, and CSV merging | Handles both training-scale and short-range inference data |
| **API Layer** | `/dataset/{lat}/{lon}` route expanded with query parameters | Supports flexible date ranges and descriptive error handling |
| **Storage Layer** | `/data/raw/` structured as persistent cache directory | Enables offline re-use for model training and experimentation |

---

### Next Planned Step  

- Implement **structured logging** using Python’s `logging` module:  
  - Log dataset fetches, cache hits, and failures to `logs/dataset_fetch.log`.  
  - Include metadata such as timestamp, coordinates, date range, and status.  
- Prepare `/preprocess` to consume cached CSVs directly for model-ready feature creation.  

---

### Summary  

The dataset service now acts as a robust **data ingestion and caching layer** for the *“Will It Rain?”* backend.  
It bridges real-world NASA climate data with the project’s training and prediction workflows — providing both reliability and flexibility.  

By combining chunked retrieval, caching, and dynamic date ranges, the backend can now support model development at scale while remaining API-compliant and hackathon-optimized.  

> *End of log entry — October 5, 2025*

# 🌦️ Backend Pipeline Overview

## NASA Space Apps 2025 – *“Will It Rain?”*

---

## 🧩 Purpose

The backend pipeline powers the *“Will It Rain?”* application by connecting user input (location) to scientific datasets and machine learning predictions.  
This document provides a high-level overview of how the backend’s modular services work together to deliver real-time rainfall probability forecasts.

The architecture is designed for **clarity, modularity, and scientific traceability** — ensuring every step, from user input to prediction output, is explainable, testable, and repeatable.

---

## 🚀 End-to-End Data Flow

```text
User Input (City, State)
        ↓
  /location  →  OpenWeather Geocoding API
        ↓
  /dataset   →  NASA POWER CSV Download
        ↓
 /preprocess →  Feature Cleaning & Transformation
        ↓
  /predict   →  ML Model Inference (Rain Probability)
```

Each service is independent but sequentially connected, forming a streamlined data pipeline that enables location-driven weather prediction without manual intervention.

---

## 🌍 Stage 1 – Location Service  

**Route:** `/location/{city}`  
**Module:** `src/services/location_service.py`

### Purpose

Converts a city/state name into geographic coordinates (latitude & longitude) for use in NASA dataset retrieval.

### Key Functions

- Calls **OpenWeather Geocoding API** for accurate global coverage.  
- Implements **in-memory caching** (`lru_cache`) for repeated lookups.  
- Returns structured JSON containing city, coordinates, and caching status.

### Example Output

```json
{
  "city": "Denver",
  "state": "CO",
  "latitude": 39.7392,
  "longitude": -104.9903,
  "cached": true
}
```

---

## 📡 Stage 2 – Dataset Service  

**Route:** `/dataset/{lat}/{lon}`  
**Module:** `src/services/dataset_service.py`

### Purpose

Fetches and parses **NASA POWER** daily weather data for the user’s geographic coordinates.  
This service transforms location inputs into structured environmental data used for model training and prediction.

### Data Source

- **NASA POWER Project (Daily Point API)** — parameterized CSV downloads supporting:  
  - `PRECTOT` → Daily precipitation (mm/day)  
  - `T2M` → Average air temperature (°C)  
  - `RH2M` → Relative humidity (%)  

### Key Functions

- Dynamically builds NASA POWER CSV URLs from latitude, longitude, and date range.  
- Uses `httpx.AsyncClient` to download and parse CSVs directly in memory.  
- Performs validation (non-empty, expected columns).  
- Returns a Pandas DataFrame or JSON summary for downstream preprocessing.

### Example Output

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

## 🧪 Stage 3 – Preprocess Service  

**Route:** `/preprocess`  
**Module:** `src/services/preprocess_service.py`

### Purpose

Cleans, standardizes, and enhances the raw NASA POWER dataset before it is passed into the machine-learning model.  
This service ensures that the data is valid, consistent, and feature-rich, aligning perfectly with the model’s expected schema.

### Key Functions

- Removes missing or invalid rows and normalizes all numeric fields.  
- Converts measurement units to consistent formats (e.g., °C, mm/day).  
- Generates derived features such as precipitation averages or dew-point approximations.  
- Validates final schema against the model’s required columns.  
- Logs transformation summaries for transparency during the demo.

### Example Output

```json
{
  "rows_processed": 365,
  "features": ["PRECTOT", "T2M", "RH2M", "dew_point"],
  "status": "ready"
}
```

---

## 🌧️ Stage 4 – Predict Service  

**Route:** `/predict`  
**Module:** `src/services/predict_service.py`

### Purpose

Executes the trained rainfall-prediction model to produce a probability and confidence score for a given date and location.  
This layer delivers the project’s core capability — turning processed NASA data into actionable insights.

### Key Functions

- Loads serialized model once at startup (`.joblib`, `.pkl`, or `.onnx`).  
- Accepts validated, preprocessed feature vectors from the `/preprocess` service.  
- Runs `predict_proba()` or equivalent model inference call.  
- Returns standardized JSON containing probability, confidence, and model metadata.  
- Handles invalid or incomplete inputs gracefully with clear error messages.

### Example Output

```json
{
  "rain_probability": 0.72,
  "confidence": 0.85,
  "model_version": "1.0.0",
  "features_used": ["PRECTOT", "T2M", "RH2M", "dew_point"]
}
```

---

## 🔄 Integration Summary  

| Service | Input | Output | Description |
|----------|--------|---------|-------------|
| **Location Service** | City & State | Latitude & Longitude | Converts user-provided city/state into geographic coordinates using the OpenWeather Geocoding API. |
| **Dataset Service** | Latitude & Longitude | Raw weather data (CSV → DataFrame) | Retrieves NASA POWER daily climate data as CSV and parses it into a DataFrame for analysis. |
| **Preprocess Service** | Raw DataFrame | Clean, standardized dataset | Cleans, normalizes, and enriches the dataset for model readiness. |
| **Predict Service** | Processed DataFrame | Rain probability & confidence | Generates rainfall predictions with confidence metrics using the trained model. |

Each stage is designed to communicate through validated schemas, maintaining strict data integrity and traceability from user input to final model output.  
This modular structure ensures that any single component can be tested, replaced, or enhanced independently without disrupting the overall system.

---

## 🧩 Backend Design Principles  

| Principle | Description |
|------------|-------------|
| **Asynchronous I/O** | Non-blocking network calls using `httpx.AsyncClient` ensure responsive data retrieval from NASA and OpenWeather endpoints. |
| **Modular Architecture** | Each logical component (location, dataset, preprocess, predict) is isolated in its own service within `src/services/`. |
| **Caching Layer** | In-memory `lru_cache` currently implemented; Redis support planned for scalability and persistence. |
| **Test-Driven Development** | Async pytest suite validates each endpoint and integration flow, ensuring confidence before merging to `integration` branch. |
| **Configuration Management** | Environment variables managed through Pydantic `BaseSettings`, enabling easy switching between development and production modes. |
| **Hackathon Optimization** | Lightweight, Docker-friendly design minimizes setup time and supports local demo deployment. |

---

## 🧠 Future Enhancements  

| Category | Enhancement | Benefit |
|-----------|--------------|----------|
| **Data Expansion** | Add NOAA or ECMWF datasets for ensemble predictions. | Broader coverage and model robustness. |
| **Caching Improvements** | Implement Redis-based caching for NASA POWER requests and preprocessed outputs. | Faster repeat queries and reduced API calls. |
| **Model Explainability** | Integrate SHAP or LIME with `/predict` for interpretable AI. | Enhances transparency and credibility for judges. |
| **Deployment Simplification** | Add Docker Compose stack and CI/CD pipeline for automated builds. | One-command startup and continuous integration. |
| **Monitoring and Logging** | Include structured logging, timing metrics, and alerting for failures. | Improved observability and debugging during demo. |

---

## ✅ Backend Completion Milestones  

| Stage | Status | Notes |
|--------|---------|-------|
| `/location` | ✅ Complete | Geocoding API integrated and tested successfully. |
| `/dataset` | 🚧 In Progress | NASA POWER integration under active development. |
| `/preprocess` | 🚧 Pending | Feature engineering and schema validation planned next. |
| `/predict` | 🚧 Planned | Will connect with Ainesh’s trained ML model for inference. |
| **Testing Framework** | ✅ Complete | Async pytest suite passing; CI integrated. |
| **Documentation** | ✅ Complete | All backend service plans and architecture finalized. |

---

## 💡 Summary  

The backend of *“Will It Rain?”* provides a fully modular, asynchronous, and data-driven architecture that connects user input with open NASA datasets and machine-learning predictions.  
This pipeline demonstrates the complete transformation of **user intent (location)** into **scientific insight (rain probability)**, powered by transparent data retrieval and rigorous preprocessing.

Each service — from `/location` through `/predict` — can be independently maintained, tested, or extended, making the backend both **hackathon-optimized** and **production-ready** for future iterations.  

When integrated with the frontend UI, users will be able to input any global location and instantly receive a predictive rainfall probability backed by NASA data science and AI.

---

**Prepared by:**  
**Brice Nelson**  
*Backend & Infrastructure Lead – NASA Space Apps 2025 “Will It Rain?”*

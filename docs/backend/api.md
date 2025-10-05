# API Documentation

This document provides an overview of the backend API for the "Will It Rain?" project. The API is built using FastAPI and provides endpoints for location services and weather data retrieval.

## Date: 2025-10-05

## 🛰️ Backend Progress Report

### NASA Space Apps 2025 – *“Will It Rain?”*

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

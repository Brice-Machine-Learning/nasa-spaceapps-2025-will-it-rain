# 🧪 Preprocess Service Plan

## NASA Space Apps 2025 – *“Will It Rain?”*

## Component: Backend Data Preparation Layer

---

## 🧩 Purpose

The **Preprocess Service** transforms raw NASA POWER weather data into a clean, feature-ready dataset for the machine learning model.  
It acts as the critical bridge between data ingestion (`/dataset`) and model inference (`/predict`), ensuring the model receives standardized, validated inputs.

This service focuses on **data quality, feature consistency, and schema enforcement**, all essential for reproducible and reliable rainfall predictions.

---

## 🧠 Design Philosophy

- **Deterministic**: The same input CSV should always yield the same feature set.  
- **Modular**: Each transformation step (cleaning, scaling, feature creation) should be independently testable.  
- **Transparent**: Log key preprocessing decisions for traceability during hackathon demos.  
- **Model-Aware**: Output format and columns must align precisely with what the ML model expects.

---

## ⚙️ Functional Overview

| Step | Description | Output |
|------|--------------|--------|
| **1. Input** | Accepts a raw dataset (as a DataFrame or CSV file path) retrieved from the NASA POWER API. | Raw DataFrame |
| **2. Cleaning** | Removes non-numeric columns, fills or interpolates missing values, and ensures consistent units (e.g., °C for temperature, mm/day for precipitation). | Cleaned DataFrame |
| **3. Feature Engineering** | Derives new features relevant to rainfall prediction such as moving averages, relative humidity indices, or lagged precipitation values. | Feature-enriched DataFrame |
| **4. Normalization & Scaling** | Scales numerical features into model-compatible ranges (e.g., MinMaxScaler or StandardScaler if required). | Scaled DataFrame |
| **5. Validation** | Confirms that all required model columns exist and no NaN values remain. | Validated dataset ready for prediction |
| **6. Output** | Returns a processed dataset or summary JSON, depending on context (internal use or API response). | JSON summary or DataFrame |

---

## 📦 File Location

- `src/services/preprocess_service.py` – Main service logic.

---

## 🧰 Responsibilities

1. **Data Cleaning**
   - Drop unnecessary metadata or header rows included in NASA CSVs.
   - Handle missing or invalid numeric values using interpolation or mean imputation.
   - Convert date columns into a unified `datetime` index for temporal alignment.

2. **Feature Creation**
   - Compute rolling averages (e.g., 3-day precipitation mean).  
   - Derive temperature/humidity interaction features (e.g., dew point approximation).  
   - Flag potential “rain events” as binary or categorical indicators for the model.

3. **Feature Normalization**
   - Ensure all model inputs share consistent scales and units.  
   - Store scalers (e.g., via `joblib`) for reproducibility.

4. **Schema Enforcement**
   - Check against a fixed schema or template (e.g., `model_input_columns = ['PRECTOT', 'T2M', 'RH2M', 'dew_point']`).  
   - Raise structured errors if key columns are missing.

5. **Logging**
   - Generate transformation summaries (rows dropped, features added, missing values filled).  
   - Provide optional JSON summary for debugging in `/preprocess` route response.

---

## 🧩 Integration Points

| Component | Interaction |
|------------|-------------|
| **`/dataset` Route** | Supplies raw DataFrame or CSV from NASA POWER dataset. |
| **`preprocess_service`** | Performs data transformations and schema alignment. |
| **`/predict` Endpoint** | Consumes the processed DataFrame for model inference. |
| **Local Data Layer (`data/processed/`)** | Optional storage location for preprocessed datasets (for debugging and offline use). |

---

## 🧠 Future Enhancements

| Feature | Description | Benefit |
|----------|--------------|----------|
| **Dynamic Feature Configuration** | Allow feature set to be defined in a JSON config file for easy updates. | Enables quick iteration during hackathon. |
| **Automated Unit Normalization** | Detect and convert units automatically (°C → K, mm/day → cm/day). | Prevents inconsistent model input scales. |
| **Feature Selection via ML Importance** | Integrate SHAP or feature importance metrics to prune unnecessary inputs. | Improves efficiency and interpretability. |
| **Model-Aware Schema Adaptation** | Automatically align preprocessing pipeline with the model’s saved feature schema. | Reduces risk of schema mismatch during integration. |
| **Preprocessing Caching** | Store intermediate results to skip repeated transformations for the same dataset. | Accelerates repeated predictions. |

---

## ✅ Success Criteria

| Criterion | Target |
|------------|---------|
| **Data Integrity** | No missing or invalid values remain post-cleaning. |
| **Schema Match** | Final dataset columns match the model’s expected input schema. |
| **Consistency** | Identical inputs yield identical processed outputs. |
| **Performance** | Preprocessing completes within 1–2 seconds for standard daily datasets. |
| **Transparency** | Transformation logs and summaries are accessible for review. |

---

## 🧾 Testing & Validation Strategy

1. **Unit Tests**
   - Validate handling of missing values, type conversions, and feature derivations.
   - Confirm deterministic outputs for given inputs.

2. **Integration Tests**
   - Connect `/dataset` → `/preprocess` routes in a test pipeline.
   - Assert successful handoff and compatible output schema.

3. **Regression Tests**
   - Verify that model predictions remain stable after preprocessing changes.

---

## 🧩 Deliverables Summary

| Deliverable | Description | Status |
|--------------|--------------|--------|
| **`preprocess_service.py`** | Core module performing data cleaning and feature engineering. | 🚧 Planned |
| **`/preprocess` Route** | API wrapper exposing preprocessing pipeline for integration and testing. | 🚧 Pending |
| **Test Suite (`test_preprocess_service.py`)** | Covers transformations, schema validation, and output consistency. | ☐ To be developed |
| **Documentation (this file)** | Full design specification of the preprocessing layer. | ✅ Complete |

---

## 💡 Summary

The **Preprocess Service** standardizes and enhances raw NASA POWER data, ensuring it’s ready for machine learning inference.  
By automating cleaning, feature creation, and validation, it guarantees that model inputs are accurate, consistent, and reproducible.  

This service will form the **data integrity backbone** of the backend pipeline, connecting dataset retrieval with the rainfall prediction engine in a reliable, transparent, and performance-oriented way.

---

**Prepared by:**  
**Brice Nelson**  
*Backend & Infrastructure Lead – NASA Space Apps 2025 “Will It Rain?”*

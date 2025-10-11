# 🌧️ Predict Service Plan

## NASA Space Apps 2025 – *“Will It Rain?”*

## Component: Backend Model Inference Layer

---

## 🧩 Purpose

The **Predict Service** is the final stage of the backend pipeline.  
It receives a fully preprocessed dataset from the `/preprocess` service and uses the trained machine learning model to generate rainfall predictions for a specific location and date.

This layer transforms data into insight — turning cleaned weather variables into interpretable, probability-based predictions.  

It will serve as the **core of the MVP**, delivering real-time rainfall likelihood for any given location.

---

## 🧠 Design Philosophy

- **Separation of Concerns** – Keep model logic isolated from API routes.  
- **Transparency** – Return both the predicted class (rain/no rain) and model confidence/probability.  
- **Efficiency** – Load model once at startup (not per request) to minimize latency.  
- **Resilience** – Handle missing data, invalid input, or model errors gracefully.  

---

## ⚙️ Functional Overview

| Step | Description | Output |
|------|--------------|--------|
| **1. Input** | Receives a processed feature vector from `/preprocess` service or frontend payload. | Dictionary or Pandas DataFrame of features |
| **2. Model Loading** | Loads the trained rainfall prediction model (e.g., `.joblib`, `.pkl`, or `.onnx`). Cached in memory for reuse. | In-memory model object |
| **3. Prediction Execution** | Feeds the input features into the model’s `predict_proba()` or equivalent method. | Probability of rain (0–1 float) |
| **4. Confidence Scoring** | Extracts model confidence or uncertainty metrics (where supported). | Confidence float |
| **5. Output Formatting** | Returns standardized JSON output for the API route. | JSON response with probabilities and metadata |

---

## 📦 File Location

- `src/services/predict_service.py` – Main service logic.

---

## 🧰 Responsibilities

1. **Model Management**
   - Load the trained ML model (provided by Ainesh) at startup.
   - Support multiple serialization formats (`.joblib`, `.pkl`, `.onnx`).
   - Store model path in environment variable or settings file for flexibility.

2. **Prediction Pipeline**
   - Accept validated input from preprocessing step.
   - Convert data to numpy arrays or tensors (depending on model type).
   - Perform forward pass through model and extract probabilities.

3. **Result Packaging**
   - Convert numerical outputs into interpretable format (rain/no rain, confidence).
   - Include metadata such as timestamp, model version, and feature importance (if applicable).

4. **Error Handling**
   - Gracefully manage missing features or unexpected input schema.
   - Return structured error messages instead of stack traces.

5. **Performance Optimization**
   - Keep the model in memory across requests.
   - Consider lightweight model variants if latency becomes a concern.

---

## 🧩 Integration Points

| Component | Interaction |
|------------|-------------|
| **`/preprocess` Service** | Supplies the cleaned and feature-engineered input DataFrame. |
| **`predict_service`** | Loads the model and generates prediction probabilities. |
| **`/predict` Route** | API endpoint that wraps the predict service and exposes the results to the frontend. |
| **Frontend/UI** | Displays rain probability, confidence, and feature summaries. |
| **Logs/Analytics** | Records prediction results for analysis or model retraining insights. |

---

## 🧠 Future Enhancements

| Feature | Description | Benefit |
|----------|--------------|----------|
| **Model Versioning** | Tag predictions with model version number to track updates. | Improves reproducibility and auditability. |
| **Explainability (SHAP / LIME)** | Include feature contributions in API response for interpretability. | Helps explain why the model predicts rain. |
| **Batch Predictions** | Allow multiple date/location requests in a single call. | Efficient data exploration for researchers. |
| **Streaming Integration** | Adapt prediction pipeline for real-time or scheduled updates (e.g., hourly forecasts). | Enables continuous monitoring capabilities. |
| **Model Refresh Endpoint** | Add admin route to reload updated models dynamically without server restart. | Facilitates iterative model tuning during hackathon. |

---

## ✅ Success Criteria

| Criterion | Target |
|------------|---------|
| **Model Integration** | Model loads successfully and is callable via `/predict`. |
| **Prediction Accuracy** | Predictions align with expected outputs for test datasets. |
| **Latency** | Single prediction completes in < 500ms after preprocessing. |
| **Robustness** | Handles invalid or incomplete data gracefully. |
| **Response Clarity** | Returns structured JSON with rain probability and confidence. |

---

## 🧾 Testing & Validation Strategy

1. **Unit Tests**
   - Mock model and verify correct input-output transformations.
   - Test invalid input handling and probability bounds (0–1).

2. **Integration Tests**
   - Run full pipeline test (`/location` → `/dataset` → `/preprocess` → `/predict`).
   - Validate schema continuity and prediction format.

3. **Regression Tests**
   - Confirm consistent predictions after model updates.

4. **Performance Tests**
   - Benchmark prediction speed and memory usage under load.

---

## 🧩 Deliverables Summary

| Deliverable | Description | Status |
|--------------|--------------|--------|
| **`predict_service.py`** | Service module responsible for model loading and inference. | 🚧 Planned |
| **`/predict` Route** | Public API endpoint exposing rainfall probability and confidence. | 🚧 Pending |
| **Test Suite (`test_predict_service.py`)** | Unit and integration tests for prediction accuracy and stability. | ☐ To be developed |
| **Documentation (this file)** | Design plan for inference layer integration. | ✅ Complete |

---

## 💡 Summary

The **Predict Service** transforms the backend from a data processing engine into a true **predictive intelligence system**.  
By connecting the preprocessed NASA data with the trained ML model, it enables the project’s core functionality — predicting rainfall probability for any given location and date.

Once integrated, this service will complete the backend pipeline:
> `/location` → `/dataset` → `/preprocess` → `/predict`

This marks the transition from infrastructure setup to full-feature MVP delivery for the hackathon presentation.

---

**Prepared by:**  
**Brice Nelson**  
*Backend & Infrastructure Lead – NASA Space Apps 2025 “Will It Rain?”*

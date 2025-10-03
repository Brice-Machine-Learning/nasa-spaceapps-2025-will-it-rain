# 🗓️ Hackathon 48-Hour Milestones  

## Day 1 – Foundations & Core Build

### Brice (Backend & Infrastructure)

- Set up GitHub repo with CI/CD basics (linting, tests, workflow).  
- Scaffold backend (FastAPI/Flask) with a placeholder `/predict` endpoint.  
- Define input/output schema (location + date → JSON response).  

### Ainesh (Data & Analytics)

- Gather datasets (NASA/NOAA + supplemental APIs like OpenWeather).  
- Perform initial cleaning and preprocessing.  
- Run quick exploratory analysis (EDA) to identify key weather features (temp, humidity, cloud cover, etc.).  

**Shared Milestone:**

- Align on MVP scope:  
  - One endpoint (`/predict`)  
  - One dataset pipeline  
  - One basic model (rain/no rain classification).  

✅ **End of Day 1 Goal:**  
Backend skeleton is running locally, dataset is cleaned, and first model approach is chosen.  

---

## Day 2 – Integration, Testing & Presentation

### Brice (Backend & Infrastructure)

- Connect backend to the model pipeline.  
- Add error handling, logging, and minimal visualization (e.g., Streamlit or a simple matplotlib plot).  
- Ensure repo is documented and demo-ready.  

### Ainesh (Data & Analytics)

- Train and validate first ML model (logistic regression or random forest).  
- Package model for easy integration (e.g., joblib or function wrapper).  
- Produce at least one visualization of results (probability trends, feature importance).  

**Shared Milestone:**

- End-to-end demo works: user inputs location/date → backend queries model → returns probability of rain.  
- Create a short slide deck (problem, approach, architecture, demo screenshots).  
- Do a dry run of the presentation.  

✅ **End of Day 2 Goal:**  
Working MVP + presentation/demo prepared for judges.  

---

## Stretch Goals (if time allows)

- Add “best time window” suggestions (not just yes/no).  
- Build ensemble or second model for comparison.  
- Containerize with Docker for portability.  
- Add nicer UI polish (maps, charts, dropdowns).  

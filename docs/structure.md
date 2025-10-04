# Project Structure for "Will It Rain?" NASA Space Apps 2025

nasa-spaceapps-2025-will-it-rain/
│
├── README.md
├── requirements.txt
├── docs/
│   ├── plan.md
│   ├── resources.md
│   └── architecture.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI backend
│   │   └── routes/
│   │       ├── health.py          # /health
│   │       ├── location.py        # /location
│   │       ├── dataset.py         # /dataset
│   │       ├── preprocess.py      # /preprocess
│   │       └── predict.py         # /predict
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── location_service.py    # talk to geocoding API
│   │   ├── dataset_service.py     # talk to NASA API
│   │   └── model_service.py       # orchestrates model pipeline
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── preprocess.py     # wrangling scripts
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── predictor.py      # ML model class or functions
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── notebooks/
│   └── eda.ipynb          # exploratory data analysis
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py         # FastAPI/Flask endpoint tests
│   ├── test_data.py        # data cleaning/wrangling
│   └── test_model.py       # ML model output sanity checks
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions for CI/CD
│
└── .gitignore

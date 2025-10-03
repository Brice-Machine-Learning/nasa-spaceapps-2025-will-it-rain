# Project Structure for "Will It Rain?" NASA Space Apps 2025

nasa-spaceapps-2025-will-it-rain/
│
├── README.md
├── requirements.txt           # or pyproject.toml if you prefer poetry/uv
├── src/
│   ├── api/                   # FastAPI or Flask backend
│   │   └── main.py
│   ├── data/                  # data wrangling scripts
│   │   └── preprocess.py
│   ├── models/                # ML/weather prediction logic
│   │   └── predictor.py
│   └── utils/                 # helpers (logging, config)
│
├── notebooks/                 # quick EDA and model tests
│   └── eda.ipynb
│
├── docs/
│   ├── resources.md           # links to NASA/NOAA data, APIs
│   ├── architecture.md        # diagram of data flow
│   └── pitch.md               # draft pitch/demo notes
│
└── .gitignore

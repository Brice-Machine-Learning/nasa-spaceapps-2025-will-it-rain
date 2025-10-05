"""src/api/main.py"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import get_settings
from src.api.routes import health, location

settings = get_settings()

# --- App Initialization ---
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="NASA Space Apps 2025 – Will It Rain? Backend API",
    contact={
        "name": "Team NASA Space Apps 2025",
        "url": "https://spaceappschallenge.org/",
        "email": "team@spaceapps2025.org",
    },
    license_info={"name": "MIT License"},
)


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during hackathon, open access; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routers ---
app.include_router(health.router)
app.include_router(location.router)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
def root():
    """Root route for API overview."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Welcome to the NASA Space Apps 2025 – Will It Rain? API",
    }

"""
src/utils/activity_parameters.py

Defines NASA POWER variable mappings for activity-based weather data selection.
Each user activity corresponds to a curated subset of meteorological parameters,
optimized for the "Will It Rain?" NASA Space Apps 2025 project.

These mappings should remain synchronized with:
docs/dev_diary/activity_parameter_map.md
"""

# ------------------------------------------------------------
# NASA POWER Parameter Definitions
# ------------------------------------------------------------

PARAMETER_DEFINITIONS = {
    "T2M": "Air temperature at 2 meters above the surface (°C)",
    "T2M_MAX": "Maximum daily air temperature at 2 meters (°C)",
    "T2M_MIN": "Minimum daily air temperature at 2 meters (°C)",
    "RH2M": "Relative humidity at 2 meters (%)",
    "PRECTOTCORR": "Corrected total daily precipitation (mm/day)",
    "ALLSKY_KT": "Clearness index (ratio of actual to clear-sky radiation, 0–1)",
    "ALLSKY_SFC_SW_DWN": "All-sky surface shortwave downward irradiance (W/m²)",
    "WS2M": "Wind speed at 2 meters above the surface (m/s)",
    "WS10M": "Wind speed at 10 meters above the surface (m/s)",
    "WD10M": "Wind direction at 10 meters above the surface (degrees 0–360)",
    "EVLAND": "Land surface evapotranspiration (mm/day)",
    "GWETROOT": "Root-zone soil wetness (fraction of saturation 0–1)",
}

# ------------------------------------------------------------
# Activity-to-Parameter Mapping
# ------------------------------------------------------------

ACTIVITY_PARAMS = {
    # Outdoor recreation
    "camping": "T2M,T2M_MAX,T2M_MIN,RH2M,PRECTOTCORR,ALLSKY_KT,WS2M",
    "beach": "T2M_MAX,ALLSKY_SFC_SW_DWN,ALLSKY_KT,WS2M,RH2M",
    "running": "T2M,T2M_MAX,RH2M,WS2M,PRECTOTCORR",

    # Water-based activities
    "boating": "PRECTOTCORR,WS10M,WD10M,T2M,RH2M,ALLSKY_KT",

    # Visual / observation activities
    "photography": "ALLSKY_KT,ALLSKY_SFC_SW_DWN,T2M,RH2M,PRECTOTCORR",

    # Environmental & occupational
    "agriculture": "PRECTOTCORR,T2M,RH2M,ALLSKY_SFC_SW_DWN,EVLAND,GWETROOT",
    "aviation": "WS10M,WD10M,PRECTOTCORR,ALLSKY_KT,T2M",

    # Events & gatherings
    "outdoor_wedding": "PRECTOTCORR,ALLSKY_KT,ALLSKY_SFC_SW_DWN,T2M_MAX,RH2M,WS2M",
}

# ------------------------------------------------------------
# Optional Aliases for User-Friendly Input
# ------------------------------------------------------------

ACTIVITY_ALIASES = {
    "hiking": "camping",
    "fishing": "boating",
    "sailing": "boating",
    "stargazing": "photography",
    "gardening": "agriculture",
    "drone": "aviation",
    "wedding": "outdoor_wedding",
    "party": "outdoor_wedding",
    "reception": "outdoor_wedding",
}

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def get_parameters_for_activity(activity: str) -> str:
    """
    Return the comma-separated NASA POWER parameters string for a given activity.
    Falls back to alias resolution where applicable.
    """
    key = activity.lower().strip()
    key = ACTIVITY_ALIASES.get(key, key)
    return ACTIVITY_PARAMS.get(key)


def describe_parameter(code: str) -> str:
    """Return a human-readable description for a NASA POWER parameter code."""
    return PARAMETER_DEFINITIONS.get(code, "Unknown parameter code")

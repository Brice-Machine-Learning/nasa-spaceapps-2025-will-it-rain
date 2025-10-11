---
title: "Activity-to-Parameter Mapping for Weather Modeling"
date: 2025-10-11
author: Brice Nelson
role: Backend & Infrastructure Lead
project: NASA Space Apps 2025 – "Will It Rain?"
---

# Activity-to-Parameter Mapping for Weather Modeling
**Date:** October 11, 2025  
**Author:** Brice Nelson  
**Role:** Backend & Infrastructure Lead  
**Project:** NASA Space Apps 2025 – "Will It Rain?"  

---

## 🌦️ Overview

This document defines how user-selected activities correspond to curated NASA POWER climate parameters.  
Each activity is associated with a specific set of meteorological variables chosen to capture the weather conditions that matter most to that use case.

These parameter bundles will be used by the `/dataset` endpoint to dynamically select which NASA POWER features to retrieve and store for the model pipeline.

---

## 🧭 Context

NASA POWER provides a broad range of satellite-based climate variables, including temperature, precipitation, humidity, wind, and solar irradiance.  
To make the data meaningful for user-specific activities, this project groups parameters by context — focusing on comfort, safety, and suitability for planned outdoor events.

---

## 🧱 Activity Summary Table

| Activity | Key Parameters | Rationale |
|-----------|----------------|------------|
| **Camping / Hiking** | `T2M`, `T2M_MAX`, `T2M_MIN`, `RH2M`, `PRECTOTCORR`, `ALLSKY_KT`, `WS2M` | Campers need to avoid rain, ensure comfortable temperatures, and anticipate wind and sky conditions. The clearness index (`ALLSKY_KT`) and precipitation capture sunlight and dryness, while humidity and temperature range define comfort. |
| **Beach / Swimming** | `T2M_MAX`, `ALLSKY_SFC_SW_DWN`, `ALLSKY_KT`, `WS2M`, `RH2M` | Warmth and clear skies define a good beach day. Solar irradiance and clearness index measure sunlight, while temperature and humidity influence comfort. Wind provides surf and cooling effects but can affect safety. |
| **Running / Outdoor Exercise** | `T2M`, `T2M_MAX`, `RH2M`, `WS2M`, `PRECTOTCORR` | Runners care about thermal comfort and dryness. Precipitation and wind affect safety; temperature and humidity affect endurance and heat stress. |
| **Boating / Sailing / Fishing** | `PRECTOTCORR`, `WS10M`, `WD10M`, `T2M`, `RH2M`, `ALLSKY_KT` | Wind direction and speed determine water conditions. Rain and visibility (via clearness index) affect safety and navigation, while temperature and humidity contribute to comfort. |
| **Photography / Stargazing** | `ALLSKY_KT`, `ALLSKY_SFC_SW_DWN`, `T2M`, `RH2M`, `PRECTOTCORR` | Clear skies and good light are essential. The clearness index and irradiance quantify sky clarity, while humidity and rain impact lens fogging and visibility. |
| **Agriculture / Gardening** | `PRECTOTCORR`, `T2M`, `RH2M`, `ALLSKY_SFC_SW_DWN`, `EVLAND`, `GWETROOT` | Crop growth depends on sunlight, moisture, and temperature. Precipitation, soil wetness, and evapotranspiration drive water balance, while radiation measures photosynthetic potential. |
| **Aviation / Drone Flying** | `WS10M`, `WD10M`, `PRECTOTCORR`, `ALLSKY_KT`, `T2M` | Pilots and drone operators depend on wind stability, visibility, and dryness. Wind direction/speed and precipitation are safety-critical; temperature aids density altitude assessment. |
| **Outdoor Wedding / Reception / Party** | `PRECTOTCORR`, `ALLSKY_KT`, `ALLSKY_SFC_SW_DWN`, `T2M_MAX`, `RH2M`, `WS2M` | Comfort, lighting, and dryness are key. Rain and humidity affect guest experience; sunlight and clearness index indicate brightness for photos; temperature and wind determine comfort. |

---

## 📘 NASA POWER Parameter Reference

| Code | Description | Units | Category |
|------|--------------|--------|-----------|
| **T2M** | Air temperature at 2 meters above the surface | °C | Temperature |
| **T2M_MAX** | Maximum daily air temperature at 2 meters | °C | Temperature |
| **T2M_MIN** | Minimum daily air temperature at 2 meters | °C | Temperature |
| **RH2M** | Relative humidity at 2 meters | % | Moisture |
| **PRECTOTCORR** | Corrected total daily precipitation | mm/day | Precipitation |
| **ALLSKY_KT** | Clearness index (ratio of actual to theoretical clear-sky radiation) | dimensionless (0–1) | Sky clarity / cloudiness |
| **ALLSKY_SFC_SW_DWN** | All-sky surface shortwave downward irradiance (total solar radiation reaching surface) | W/m² | Solar radiation |
| **WS2M** | Wind speed at 2 meters above the surface | m/s | Wind |
| **WS10M** | Wind speed at 10 meters above the surface | m/s | Wind |
| **WD10M** | Wind direction at 10 meters above the surface | degrees (0–360) | Wind |
| **EVLAND** | Land surface evapotranspiration | mm/day | Moisture / Energy balance |
| **GWETROOT** | Root-zone soil wetness (fraction of saturation) | fraction (0–1) | Soil moisture |

---

## 🧩 Implementation Notes

- Each activity’s parameter list is stored in a mapping dictionary (`ACTIVITY_PARAMS`) under `src/utils/activity_parameters.py`.
- The `/dataset` endpoint accepts an `activity` query parameter and uses this mapping to request only the relevant variables from NASA POWER.
- This selective data retrieval improves both performance and interpretability of the model results.

---

## 🧠 Future Enhancements

- Add *seasonal weighting* (e.g., emphasize `T2M_MIN` for winter camping).  
- Allow *user-defined activities* that map to the closest predefined bundle.  
- Use *feature-importance analysis* from trained models to refine parameter sets dynamically.  
- Integrate *real-time weather forecasts* to complement historical NASA POWER data for short-term event planning.

---

> *End of document – October 11, 2025*

---
title: "Activity-Based Parameter Mapping Implementation"
date: 2025-10-10
author: Brice Nelson
role: Backend & Infrastructure Lead
project: NASA Space Apps 2025 – "Will It Rain?"
---

# Activity-Based Parameter Mapping Implementation
**Date:** October 10, 2025  
**Author:** Brice Nelson  
**Role:** Backend & Infrastructure Lead  
**Project:** NASA Space Apps 2025 – "Will It Rain?"  

---

## 🧭 Overview

On October 10, 2025, Brice expanded the functionality of the *“Will It Rain?”* backend system to support **activity-specific weather modeling**.  
The purpose of this enhancement is to allow users to select an activity (e.g., camping, beach, running, wedding), and the backend will automatically determine which NASA POWER weather parameters are most relevant to that activity.

This implementation lays the foundation for a **context-aware weather dataset pipeline**, where the choice of features dynamically adjusts to the activity type.  
The ultimate goal is to feed these customized datasets into predictive models that assess conditions for comfort, safety, or feasibility of outdoor plans.

---

## ⚙️ Technical Work Completed

### 1. **Created Parameter Documentation**
A new Markdown document, `docs/dev_diary/activity_parameter_map.md`, was developed to record:
- Each supported user activity.
- The corresponding NASA POWER parameters.
- A rationale for why each variable was selected.
- Clear definitions for every parameter code (e.g., `T2M`, `PRECTOTCORR`, `ALLSKY_KT`, etc.).

This document now serves as the authoritative reference for both developers and modelers.

---

### 2. **Developed the Python Mapping Module**
A new utility module was added at:
```text
src/utils/activity_parameters.py
```

This file includes:
- **`ACTIVITY_PARAMS`** → Maps each user activity to a NASA POWER parameter list.  
- **`PARAMETER_DEFINITIONS`** → Descriptions and units for each parameter used.  
- **`ACTIVITY_ALIASES`** → Allows flexible user input (e.g., `?activity=wedding` or `?activity=party` both map to `outdoor_wedding`).  
- **Helper Functions:**
  - `get_parameters_for_activity(activity: str)`  
    Returns the comma-separated NASA parameter string.
  - `describe_parameter(code: str)`  
    Provides a human-readable explanation for each variable.

The mapping ensures that the `/dataset` endpoint can tailor API calls to match the context of the user’s planned activity.

---

### 3. **Planned Integration with NASA POWER Service**
The next development step involves extending the existing function:

```python
fetch_nasa_power_data(lat, lon, start=None, end=None)
```

to accept a new argument:

```python
fetch_nasa_power_data(lat, lon, start=None, end=None, parameters=None)
```

This enhancement will allow the backend to:
1. Retrieve the appropriate parameter list based on the user’s selected activity.
2. Dynamically include it in the API request to NASA POWER.
3. Store a customized CSV file containing only the relevant features for that activity.

Example integration snippet:
```python
from src.utils.activity_parameters import get_parameters_for_activity

parameters = get_parameters_for_activity(activity)
meta, df = await fetch_nasa_power_data(lat, lon, start=start, end=end, parameters=parameters)
```

---

## 📘 Example: Outdoor Wedding Profile

When a user selects `activity=outdoor_wedding`, the app will automatically use:
```text
PRECTOTCORR,ALLSKY_KT,ALLSKY_SFC_SW_DWN,T2M_MAX,RH2M,WS2M
```
These variables focus on dryness, sunlight, temperature comfort, humidity, and wind —  
all essential factors for planning an outdoor ceremony or reception.

---

## 🧠 Next Steps

1. **Update `fetch_nasa_power_data()`**
   - Add a `parameters` argument and ensure it dynamically populates the NASA POWER API query string.
   - Default to a basic feature set if no activity is provided.

2. **Enhance `/dataset` Route**
   - Modify the route to accept `activity` as a query parameter.
   - Use the activity-to-parameter mapping to fetch tailored datasets.
   - Return metadata including which parameters were used.

3. **Prepare for Model Integration**
   - Once activity-based CSVs are generated, connect them to the ML preprocessing pipeline.
   - Begin developing baseline models (e.g., rain probability classification by activity type).

---

## ✅ Outcome

By the end of this session, the system gained a flexible **activity-aware data framework**, enabling the backend to generate custom-tailored datasets for each user scenario.  
This marks a major step toward personalized, data-driven weather insights within the “Will It Rain?” platform.

---

> *End of log entry – October 10, 2025*

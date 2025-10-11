# 🧩 Dataset Debugging Log – NASA POWER API  

**Date:** 2025-10-05  
**Project:** NASA Space Apps – *“Will It Rain?”*  
**Author:** Brice Nelson  

---

## 🛰️ Summary  

During backend testing of the `/dataset/{lat}/{lon}` endpoint, the NASA POWER API returned successful HTTP 200 responses (with non-zero `content-length`) but the locally saved CSV files were empty.  

This session focused on verifying the true cause of the empty dataset issue.  
The investigation confirmed that:

- The NASA API call succeeded and returned valid CSV data (~9.7 KB),
- But the backend wrote an empty file because the response body was read incorrectly using `.text`,  
- The fix was to explicitly read and write the raw byte stream from `response.content`.

---

## 🧩 Root Cause  

| Category | Description |
|-----------|--------------|
| **Symptom** | CSV file created under `/data/raw/`, but file size = 0 B |
| **HTTP Response** | Status = 200 OK, `content-type: text/csv`, `content-length: 9739` |
| **NASA POWER Data** | Verified correct CSV when requested directly via browser |
| **Underlying Issue** | `httpx.Response.text` returned an empty string because NASA’s `text/csv` response lacked an explicit charset header |
| **Effect** | The backend wrote an empty string to disk even though the API returned bytes |

---

## ✅ Resolution  

### 1. Use `.content` instead of `.text`  

Replace:

```python
csv_text = response.text
```

with:

```python
csv_bytes = response.content
csv_text = csv_bytes.decode("utf-8", errors="ignore")
print(f"✅ Received {len(csv_bytes)} bytes from NASA POWER")
```

### 2. Save the raw bytes directly  

```python
with open(file_path, "wb") as f:
    f.write(csv_bytes)
```

### 3. Optional: Parse the text afterward  

```python
df = parse_nasa_csv(csv_text)
```

This ensures the complete NASA CSV (including metadata header) is first written intact, then parsed cleanly.

---

## 🧠 Lessons Learned  

| Topic | Insight |
|-------|----------|
| **HTTPX Behavior** | `.text` relies on the `charset` field of `Content-Type`. When missing, decoding may silently fail. |
| **NASA POWER API** | Returns `text/csv` without charset → must manually decode raw bytes. |
| **Data Integrity** | Always save the unmodified bytes before parsing, so raw data can be inspected later. |
| **Debugging Strategy** | Use `response.status_code`, `response.headers`, and `len(response.content)` to verify that the payload is non-empty before writing. |

---

## 🧩 Validation Results  

After switching to `.content.decode()` and saving raw bytes:

```text
✅ STATUS: 200
✅ Received 9739 bytes from NASA POWER
✅ Downloaded 2024 for (39.7392, -104.9903)
```

The saved CSV now contains:

```text
-BEGIN HEADER-
NASA/POWER Source Native Resolution Daily Data
...
-END HEADER-
YEAR,MO,DY,PRECTOTCORR,T2M,RH2M
2024,1,1,0.000,1.12,67.3
...
```

---

## 🧭 Next Steps  

| Priority | Task | Description |
|-----------|------|-------------|
| 1 | Confirm local CSV contains full dataset | Verify 2024 data rows exist (≈273 days) |
| 2 | Reinstate parser | Use the `parse_nasa_csv()` function with the `-END HEADER-` detection |
| 3 | Logging | Add log entry for every fetch: status, byte count, save path |
| 4 | Caching | Retain existing caching logic so subsequent requests reuse the saved CSV |
| 5 | Documentation | Merge this `.md` into the internal backend troubleshooting record |

---

## 💡 Takeaway  

This debugging session reinforced the principle:  
> “A 200 OK doesn’t guarantee data — always verify the bytes.”  

By reading raw content (`response.content`) instead of relying on `response.text`, the backend now captures the complete NASA POWER dataset reliably for downstream ML preprocessing.

---

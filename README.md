# 🌦 NASA Space Apps 2025 – Will It Rain On My Parade?

**Team Name:** Apollo Drizzle  
**Hackathon:** [NASA Space Apps Challenge 2025](https://www.spaceappschallenge.org/)  
**Challenge:** [Will It Rain On My Parade?](https://www.spaceappschallenge.org/2025/challenges/will-it-rain-on-my-parade/)  

---

## 🚀 Project Overview

Our project predicts the likelihood of rain for outdoor events using open NASA and NOAA datasets combined with simple ML models.  
The goal: provide event organizers with a clear, user-friendly forecast so no parade gets rained out.  

---

## 👥 Team

- **Brice Nelson** – Backend, APIs, repo setup  
  - 📧 [brice@devbybrice.com](mailto:brice@devbybrice.com)  
  - 💬 Discord: DarkAvenger  

- **Ainesh Balaga** – Data wrangling, modeling, EDA
  - 📧 [balagaainesh@gmail.com](mailto:balagaainesh@gmail.com)
  - 💬 Discord: abalaga

---

## 📊 Data & Resources

Datasets and APIs we are leveraging include:

- [NASA Earth Observations](https://neo.gsfc.nasa.gov/)  
- [NOAA Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/)  
- [OpenWeather API](https://openweathermap.org/api)  
- [Other resources from challenge page]  

*(See [`docs/resources.md`](docs/resources.md) for the full list with direct links.)*  

---

## 🛠 Tech Stack

- Python 3.12  
- FastAPI (backend)  
- Pandas, NumPy (data wrangling)  
- Scikit-learn (ML model)  
- Streamlit (optional quick UI)  

---

## ⚙️ How to Run

```bash
# clone the repo
git clone https://github.com/Brice-Machine-Learning/nasa-spaceapps-2025-will-it-rain
cd nasa-spaceapps-2025-will-it-rain

# install dependencies
pip install -r requirements.txt

# run backend
uvicorn src.api.main:app --reload
```

---

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) to test.  

---

## 📈 Results (MVP Goals)

- ✅ Working backend API for location/date → rain probability  
- ✅ Clean dataset pipeline (wrangling, preprocessing)  
- ✅ Simple visualization / demo (Streamlit or Matplotlib)  
- 🎯 Stretch goal: confidence bands + “best event time” suggestions  

---

## 📽 Presentation

Slides & demo link will be added here once completed.  

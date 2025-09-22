# Satellite Pass Predictor (ISS Example)

A Python project that predicts the visible passes of satellites, using the International Space Station (ISS) as an example.  
This tool fetches Two-Line Element (TLE) data from [Celestrak](https://celestrak.org), processes the orbital data with the `skyfield` library, and computes the rise, peak, and set times of visible passes over a given location.  

---

## ✨ Features
- Retrieves up-to-date TLE data from Celestrak.
- Predicts satellite passes over a user-defined latitude/longitude.
- Outputs rise, peak, and set times in **local time** with altitude information.
- Example: predictions for the ISS in Atlanta, GA.

---

## 📦 Requirements
Make sure you have Python 3.9+ installed, then install dependencies with:

```bash
pip install skyfield tzdata requests

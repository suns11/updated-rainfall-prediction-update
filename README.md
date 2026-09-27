# Bangladesh Smart Rainfall & Agriculture System

AI-based rainfall prediction and smart irrigation recommendation system.

## Features

- Rainfall Prediction
- CatBoost Model
- Weather API Integration
- Historical Weather Data
- Advanced Analytics
- Smart Agriculture
- Smart Irrigation Calculation

## Project Structure

```text
Bangladesh_Smart_Rainfall_Agriculture_System/

├── app.py
├── requirements.txt
├── README.md
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── services/
│   ├── __init__.py
│   ├── agriculture.py
│   ├── data_loader.py
│   ├── test_voice.py
│   ├── voice_input.py
│   ├── voice.py
│   └── weather_api.py
│
├── views/
│   ├── __init__.py
│   ├── about.py
│   ├── agriculture.py
│   ├── analytics.py
│   ├── data_page.py
│   ├── home.py
│   └── prediction.py
│
├── data/
│   ├── 01_bangladesh_crop_water_reference.csv
│   ├── 02_crop_kc_reference.csv
│   ├── 03_bangladesh_crop_calendar.csv
│   ├── 04_bangladesh_location_iwr_reference.csv
│   └── bangladesh_weather_stations_FINAL.csv
│
├── models/
│   └── rainfall_model.pkl
│
├── assets/
│
├── voice_cache/
│
├── .gitignore
│
└── ORIGINAL_CODE/
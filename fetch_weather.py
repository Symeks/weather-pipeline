import requests
import pandas as pd
from datetime import datetime

# API abrufen
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m,precipitation",
    "forecast_days": 7
}

response = requests.get(url, params=params)
data = response.json()

# EXTRACT – Daten laden
df = pd.DataFrame({
    "timestamp": data["hourly"]["time"],
    "temperature_c": data["hourly"]["temperature_2m"],
    "precipitation_mm": data["hourly"]["precipitation"]
})

# TRANSFORM – Daten verbessern
df["timestamp"] = pd.to_datetime(df["timestamp"])   # richtiger Datumstyp
df["date"] = df["timestamp"].dt.date                # nur Datum
df["hour"] = df["timestamp"].dt.hour                # nur Stunde
df["is_raining"] = df["precipitation_mm"] > 0       # True/False ob Regen

# LOAD – als CSV speichern
filename = f"weather_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)
print(f"\nGespeichert als: {filename}")
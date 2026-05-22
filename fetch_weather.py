import requests
import pandas as pd
import boto3
from datetime import datetime
from io import StringIO

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

# EXTRACT
df = pd.DataFrame({
    "timestamp": data["hourly"]["time"],
    "temperature_c": data["hourly"]["temperature_2m"],
    "precipitation_mm": data["hourly"]["precipitation"]
})

# TRANSFORM
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["is_raining"] = df["precipitation_mm"] > 0

# LOAD – nach S3
filename = f"weather_{datetime.now().strftime('%Y%m%d')}.csv"
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3 = boto3.client("s3")
s3.put_object(
    Bucket="weather-pipeline-stephan",
    Key=f"raw/{filename}",
    Body=csv_buffer.getvalue()
)

print(f"Erfolgreich nach S3 hochgeladen: raw/{filename}")
print(df.head(10))
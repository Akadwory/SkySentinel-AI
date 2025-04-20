import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine

# Define paths and database details
BASE_PATH = "/Users/adamkadwory/Desktop/skysentineAI/data/"
RAW_DATA_PATH = os.path.join(BASE_PATH, "raw_flight_data.csv")
CLEANED_DATA_PATH = os.path.join(BASE_PATH, "cleaned_flight_data.csv")
DB_NAME = "flight_data"
DB_USER = "adamkadwory"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "erin_123")  # Default if env var not set
DB_HOST = "localhost"
DB_PORT = "5432"

os.makedirs(BASE_PATH, exist_ok=True)

# Fetch data from PostgreSQL
print("Fetching raw flight data from PostgreSQL...")
try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_sql("SELECT icao24, callsign, latitude, longitude, geo_altitude, baro_altitude, velocity, vertical_rate, on_ground, true_track, origin_country, time_position, last_contact FROM flight_data", engine)
    print(f"Loaded {len(df)} rows.")
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

if not os.path.exists(RAW_DATA_PATH):
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Raw data saved to: {RAW_DATA_PATH}")

# Handle Missing Values for Prediction Fields
print("Preprocessing for predictive anomaly detection...")
df.fillna({
    "geo_altitude": df["geo_altitude"].median(),
    "baro_altitude": df["baro_altitude"].median(),
    "velocity": df["velocity"].median(),
    "vertical_rate": df["vertical_rate"].median(),
    "origin_country": "Unknown",
    "callsign": "Unknown"
}, inplace=True)

df["latitude"] = df.groupby("callsign")["latitude"].fillna(method="ffill").fillna(method="bfill")
df["longitude"] = df.groupby("callsign")["longitude"].fillna(method="ffill").fillna(method="bfill")
df["true_track"] = df["true_track"].fillna(df["true_track"].median())
df.dropna(subset=["latitude", "longitude", "time_position"], inplace=True)
print(f"Cleaned critical fields, rows: {len(df)}")

# Convert Time Fields
df["time_position"] = pd.to_datetime(df["time_position"], errors="coerce")
df["last_contact"] = pd.to_datetime(df["last_contact"], errors="coerce")
df["time_position"].fillna(df["last_contact"], inplace=True)
df.dropna(subset=["time_position"], inplace=True)

# Convert Boolean
df["on_ground"] = df["on_ground"].astype(int)

# Normalize for ML
num_features = ["geo_altitude", "velocity", "vertical_rate", "true_track"]
for feature in num_features:
    df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())
print("Normalized key features.")

# Segment Flights
print("Segmenting flights by aircraft and time gaps...")
df = df.sort_values(by=["icao24", "time_position"])
df["flight_segment"] = 0
current_segment = 0
for i in range(1, len(df)):
    prev = df.iloc[i-1]
    curr = df.iloc[i]
    if (curr["icao24"] != prev["icao24"] or
        curr["on_ground"] != prev["on_ground"] or 
        (curr["time_position"] - prev["time_position"]) > pd.Timedelta(minutes=10)):
        current_segment += 1
    df.loc[i, "flight_segment"] = current_segment
print(f"Identified {current_segment + 1} flight segments across aircraft.")

# Outlier/Anomaly Flagging
df["potential_safety_anomaly"] = df["vertical_rate"].apply(lambda x: 1 if abs(x) > 0.1 else 0)  # Sudden altitude changes
df["potential_security_anomaly"] = df["true_track"].apply(lambda x: 1 if abs(x - 0.5) > 0.25 else 0)  # Large maneuvers (normalized > ~90°)
df["potential_efficiency_anomaly"] = df.apply(lambda row: 1 if row["distance_traveled"] > 5000 and row["velocity"] < 0.3 else 0, axis=1)  # Inefficient long routes at low speed

print(f"Flagged {df['potential_safety_anomaly'].sum()} safety anomalies, {df['potential_security_anomaly'].sum()} security anomalies, {df['potential_efficiency_anomaly'].sum()} efficiency anomalies.")

# Save cleaned Data File As CSV 
df.to_csv(CLEANED_DATA_PATH, index=False)
print(f"Cleaned dataset saved to: {CLEANED_DATA_PATH}")
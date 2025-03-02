import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from geopy.distance import geodesic
import os 

# Define paths
BASE_PATH = "/Users/adamkadwory/Desktop/skysentineAI/data/"
CLEANED_DATA_PATH = os.path.join(BASE_PATH, "cleaned_flight_data.csv")
ENGINEERED_DATA_PATH = os.path.join(BASE_PATH, "engineered_flight_data.csv")

# Load Cleaned Data
print("🔄 Loading cleaned flight data...")
df = pd.read_csv(CLEANED_DATA_PATH)
print(f"✅ Loaded {len(df)} rows.")

# Sort for Sequential Features
df = df.sort_values(by=["icao24", "time_position"])

# Feature Engineering
print("🛠️ Engineering features for predictive anomalies...")

# Acceleration (Velocity Change)
df["acceleration"] = df.groupby("icao24")["velocity"].diff().fillna(0)

# Vertical Rate Change (Sudden Drops)
df["vertical_rate_change"] = df.groupby("icao24")["vertical_rate"].diff().fillna(0)

# Track Deviation (Maneuvers)
df["track_deviation"] = df.groupby("icao24")["true_track"].diff().fillna(0)
df["track_deviation"] = df["track_deviation"].apply(lambda x: min(abs(x), 360 - abs(x)))  # Normalize angle

# Distance Traveled
def compute_distance(row, prev_row):
    if prev_row is not None and pd.notna(row["latitude"]):
        return geodesic((prev_row["latitude"], prev_row["longitude"]), (row["latitude"], row["longitude"])).km
    return 0
df["distance_traveled"] = [compute_distance(df.iloc[i], df.iloc[i-1] if i > 0 else None) for i in range(len(df))]

# PCA for Clustering Anomalies
print("🔍 Performing PCA for anomaly clustering...")
pca_features = ["geo_altitude", "velocity", "vertical_rate", "acceleration", "track_deviation", "distance_traveled"]
pca_df = df[pca_features].fillna(0)
pca = PCA(n_components=2)
pca_transformed = pca.fit_transform(pca_df)
df["pca_1"] = pca_transformed[:, 0]
df["pca_2"] = pca_transformed[:, 1]

# Save
df.to_csv(ENGINEERED_DATA_PATH, index=False)
print(f"📂 Engineered dataset saved to: {ENGINEERED_DATA_PATH}")
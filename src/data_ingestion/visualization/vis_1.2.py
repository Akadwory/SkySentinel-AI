import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define paths
BASE_PATH = "/Users/adamkadwory/Desktop/skysentineAI/data/"
ENGINEERED_DATA_PATH = os.path.join(BASE_PATH, "engineered_flight_data.csv")

# Load Data
print("🔄 Loading engineered flight data...")
df = pd.read_csv(ENGINEERED_DATA_PATH)
print(f"✅ Loaded {len(df)} rows.")

# Visualization 1: Sample Flight Paths
sample_icao24 = df["icao24"].unique()[:5]
plt.figure(figsize=(12, 8))
for icao in sample_icao24:
    flight = df[df["icao24"] == icao]
    plt.plot(flight["longitude"], flight["latitude"], label=icao)
plt.title("Sample Flight Paths (Potential Deviations)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.savefig(os.path.join(BASE_PATH, "flight_paths.png"))
plt.close()

# Visualization 2: Vertical Rate Change by Altitude
plt.figure(figsize=(10, 6))
sns.scatterplot(x="geo_altitude", y="vertical_rate_change", hue="on_ground", data=df)
plt.title("Vertical Rate Change vs. Altitude")
plt.savefig(os.path.join(BASE_PATH, "vertical_rate_change_vs_altitude.png"))
plt.close()

# Visualization 3: PCA Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x="pca_1", y="pca_2", hue="track_deviation", size="vertical_rate_change", data=df)
plt.title("PCA Clusters with Track Deviation and Vertical Rate Change")
plt.savefig(os.path.join(BASE_PATH, "pca_anomaly_clusters.png"))
plt.close()

print("✅ Visualization outputs saved.")
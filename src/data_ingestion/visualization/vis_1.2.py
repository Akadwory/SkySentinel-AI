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

# Visualization 1: Anomaly-Highlighted Flight Paths (Per Flight Segment)
sample_icao24 = df["icao24"].unique()[:2]  # Reduce for clarity
plt.figure(figsize=(12, 8))
for icao in sample_icao24:
    flights = df[df["icao24"] == icao].groupby("flight_segment")
    for segment, flight in flights:
        color = "red" if any(flight["potential_security_anomaly"]) else "blue"
        plt.plot(flight["longitude"], flight["latitude"], label=f"{icao}_Seg{segment}", color=color, alpha=0.5)
plt.title("Sample Flight Paths by Segment (Security Anomalies in Red)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(BASE_PATH, "segmented_flight_paths.png"))
plt.close()

# Visualization 2: Vertical Rate Change by Altitude (Safety)
plt.figure(figsize=(10, 6))
sns.scatterplot(x="geo_altitude", y="vertical_rate_change", hue="potential_safety_anomaly", data=df, palette="Reds")
plt.title("Vertical Rate Change vs. Altitude (Safety Anomalies in Red)")
plt.savefig(os.path.join(BASE_PATH, "safety_anomalies_altitude.png"))
plt.close()

# Visualization 3: PCA Clusters with Anomalies
plt.figure(figsize=(10, 6))
sns.scatterplot(x="pca_1", y="pca_2", hue="potential_security_anomaly", size="vertical_rate_change", data=df, palette="Purples")
plt.title("PCA Clusters with Security Anomalies and Vertical Rate Change")
plt.savefig(os.path.join(BASE_PATH, "pca_anomaly_clusters.png"))
plt.close()

print("✅ Visualization outputs saved with anomaly emphasis.")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define paths
BASE_PATH = "/Users/adamkadwory/Desktop/skysentineAI/data/"
ENGINEERED_DATA_PATH = os.path.join(BASE_PATH, "engineered_flight_data.csv")

# Load Engineered Data
print("🔄 Loading engineered flight data...")
df = pd.read_csv(ENGINEERED_DATA_PATH)
print(f"✅ Loaded {len(df)} rows.")

# Time Gaps and Flight Segmentation
df["time_position"] = pd.to_datetime(df["time_position"])
df["time_gap"] = df.groupby("icao24")["time_position"].diff()
df["time_gap_flag"] = df["time_gap"].apply(lambda x: 1 if pd.notna(x) and x > pd.Timedelta(minutes=10) else 0)

# Overview
print("📊 Data Overview:")
print(df.info())
print("\n🔍 Missing Values:")
print(df.isnull().sum())
print("\n📈 Summary Statistics:")
print(df.describe())

# Anomaly Analysis by Flight Segment
print("🔍 Anomaly Statistics by Flight Segment:")
safety_anomalies = df[df["potential_safety_anomaly"] == 1].groupby("flight_segment").size()
security_anomalies = df[df["potential_security_anomaly"] == 1].groupby("flight_segment").size()
efficiency_anomalies = df[df["potential_efficiency_anomaly"] == 1].groupby("flight_segment").size()
print(f"Safety Anomalies by Segment: {safety_anomalies.sum()} total, {safety_anomalies.to_dict()}")
print(f"Security Anomalies by Segment: {security_anomalies.sum()} total, {security_anomalies.to_dict()}")
print(f"Efficiency Anomalies by Segment: {efficiency_anomalies.sum()} total, {efficiency_anomalies.to_dict()}")

# Visualizations
# 1. Vertical Rate Change (Safety) by Flight Segment
plt.figure(figsize=(10, 6))
sns.histplot(df[df["potential_safety_anomaly"] == 1]["vertical_rate_change"], bins=50, kde=True, color="red")
plt.title("Distribution of Safety Anomalies (Vertical Rate Changes)")
plt.savefig(os.path.join(BASE_PATH, "safety_anomalies_dist.png"))
plt.close()

# 2. Track Deviation (Security) by Flight Segment
plt.figure(figsize=(10, 6))
sns.histplot(df[df["potential_security_anomaly"] == 1]["track_deviation"], bins=50, kde=True, color="purple")
plt.title("Distribution of Security Anomalies (Track Deviations)")
plt.savefig(os.path.join(BASE_PATH, "security_anomalies_dist.png"))
plt.close()

# 3. Distance vs. Velocity (Efficiency) by Flight Segment
plt.figure(figsize=(10, 6))
sns.scatterplot(x="distance_traveled", y="velocity", hue="potential_efficiency_anomaly", data=df, palette="Reds")
plt.title("Distance Traveled vs. Velocity (Efficiency Anomalies in Red)")
plt.savefig(os.path.join(BASE_PATH, "efficiency_anomalies_dist.png"))
plt.close()

# 4. Correlation Heatmap
numeric_cols = ["geo_altitude", "velocity", "vertical_rate", "acceleration", "track_deviation", "distance_traveled"]
plt.figure(figsize=(10, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.savefig(os.path.join(BASE_PATH, "correlation_heatmap.png"))
plt.close()

print("✅ EDA visualizations saved with anomaly focus.")
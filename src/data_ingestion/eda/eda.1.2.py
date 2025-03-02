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

# Time Gaps
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

# Visualizations
# 1. Vertical Rate Change (Safety)
plt.figure(figsize=(10, 6))
sns.histplot(df["vertical_rate_change"], bins=50, kde=True)
plt.title("Distribution of Vertical Rate Changes")
plt.savefig(os.path.join(BASE_PATH, "vertical_rate_change_dist.png"))
plt.close()

# 2. Track Deviation (Security)
plt.figure(figsize=(10, 6))
sns.histplot(df["track_deviation"], bins=50, kde=True)
plt.title("Distribution of Track Deviations")
plt.savefig(os.path.join(BASE_PATH, "track_deviation_dist.png"))
plt.close()

# 3. Distance vs. Velocity (Efficiency)
plt.figure(figsize=(10, 6))
sns.scatterplot(x="distance_traveled", y="velocity", hue="on_ground", data=df)
plt.title("Distance Traveled vs. Velocity")
plt.savefig(os.path.join(BASE_PATH, "distance_vs_velocity.png"))
plt.close()

# 4. Correlation Heatmap
numeric_cols = ["geo_altitude", "velocity", "vertical_rate", "acceleration", "track_deviation", "distance_traveled"]
plt.figure(figsize=(10, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.savefig(os.path.join(BASE_PATH, "correlation_heatmap.png"))
plt.close()

print("✅ EDA visualizations saved.")
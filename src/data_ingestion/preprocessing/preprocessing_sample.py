import pandas as pd
import numpy as np
import os

# Define paths
data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/"
input_file = os.path.join(data_path, "sampled_flight_data.csv")
output_file = os.path.join(data_path, "cleaned_flight_data.csv")

#Load Data
print("Loading sampled flight data...")
df = pd.read_csv(input_file)

#Handle Missing Values
df.fillna({
    "geo_altitude": df["geo_altitude"].median(),
    "baro_altitude": df["baro_altitude"].median(),
    "velocity": df["velocity"].median(),
    "vertical_rate": df["vertical_rate"].median(),
    "origin_country": "Unknown",
    "callsign": "Unknown"
}, inplace=True)

print("Missing values handled.")

# ================================
#Convert Time Fields Properly
# ================================
if pd.api.types.is_numeric_dtype(df["time_position"]):
    df["time_position"] = pd.to_datetime(df["time_position"], unit='s', errors="coerce")
else:
    print("time_position is not in the expected numeric format. Check source data.")

if pd.api.types.is_numeric_dtype(df["last_contact"]):
    df["last_contact"] = pd.to_datetime(df["last_contact"], unit='s', errors="coerce")
else:
    print("last_contact is not in the expected numeric format. Check source data.")

#Fill Missing time_position with last_contact where possible
df["time_position"].fillna(df["last_contact"], inplace=True)

#Validate Time Conversion
missing_time_pos = df["time_position"].isna().sum()
missing_last_contact = df["last_contact"].isna().sum()
print(f"Missing time_position after fix: {missing_time_pos}")
print(f"Missing last_contact after fix: {missing_last_contact}")

# ================================
#Convert Boolean Features
# ================================
df["on_ground"] = df["on_ground"].astype(int)

# ================================
#Normalize Numerical Data
# ================================
num_features = ["geo_altitude", "baro_altitude", "velocity", "vertical_rate"]
df[num_features] = df[num_features].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# ================================
#Save Cleaned Data (Overwrite or Versioning)
# ================================
if os.path.exists(output_file):
    print("⚠️ Overwriting existing cleaned data file.")
else:
    print("Creating new cleaned dataset.")

df.to_csv(output_file, index=False)
print(f"Cleaned dataset saved at: {output_file}")

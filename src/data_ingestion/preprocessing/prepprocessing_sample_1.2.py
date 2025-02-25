import numpy as np 
import pandas as pd 
import os 


# Define paths
data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/"
input_file = os.path.join(data_path, "sampled_flight_data.csv")
output_file = os.path.join(data_path, "cleaned_flight_data.csv")


# load the data 
print("loading sample flight data ...")
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

#**Hybrid Approach for Missing Latitude & Longitude**
#If aircraft is on the ground, fill missing latitude/longitude with last known position.

df["latitude"] = df.groupby("callsign")["latitude"].fillna(method="ffill")
df["longitude"] = df.groupby("callsign")["longitude"].fillna(method="ffill")


#Drop rows where latitude & longitude are still missing for in-motion aircraft
df.dropna(subset=["latitude", "longitude"], inplace=True)
print("GPS Data Handling Completed.")

#Convert Time Fields
df["time_position"] = pd.to_datetime(df["time_position"], errors="coerce")
df["last_contact"] = pd.to_datetime(df["last_contact"], errors="coerce")
df["time_position"].fillna(df["last_contact"], inplace=True)

#Convert Boolean Features
df["on_ground"] = df["on_ground"].astype(int)

#Normalize Numerical Data
num_features = ["geo_altitude", "baro_altitude", "velocity", "vertical_rate"]
df[num_features] = df[num_features].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

#Save Cleaned Data (Overwrite or Versioning)
if os.path.exists(output_file):
    print("Overwriting existing cleaned data file.")
else:
    print("Creating new cleaned dataset.")

df.to_csv(output_file, index=False)
print(f"Cleaned dataset saved at: {output_file}")
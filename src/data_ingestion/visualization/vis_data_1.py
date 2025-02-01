import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# File path to the CSV file
file_path = "/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv"

# Load the CSV with sampling (10% of the dataset)
sample_fraction = 0.10  # Adjust this to control sample size
data = pd.read_csv(file_path).sample(frac=sample_fraction, random_state=42)

# Ensure columns are correctly typed and handle missing values
data['time_position'] = pd.to_datetime(data['time_position'], errors='coerce')
data['last_contact'] = pd.to_datetime(data['last_contact'], errors='coerce')

# Quick data overview
print(f"Total records: {len(data)}")
print("Sampled Data Overview:")
print(data.head())

# Visualization 1: Distribution of Flight Altitudes
plt.figure(figsize=(10, 6))
sns.histplot(data['geo_altitude'].dropna(), bins=50, kde=True, color='skyblue')
plt.title('Distribution of Geo Altitude (Sampled Data)')
plt.xlabel('Geo Altitude (meters)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Visualization 2: Flight Count by Origin Country
plt.figure(figsize=(12, 8))
country_counts = data['origin_country'].value_counts().head(10)
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')
plt.title('Top 10 Origin Countries by Flight Count')
plt.xlabel('Number of Flights')
plt.ylabel('Country')
plt.show()

# Visualization 3: Time-based Trend of Flights
data['hour'] = data['time_position'].dt.hour
plt.figure(figsize=(12, 6))
sns.countplot(x='hour', data=data, palette='coolwarm')
plt.title('Flight Count Distribution by Hour of Day (Sampled Data)')
plt.xlabel('Hour of Day')
plt.ylabel('Flight Count')
plt.grid(True)
plt.show()

# Visualization 4: Geo Heatmap (if data size allows)
plt.figure(figsize=(12, 8))
sns.kdeplot(
    x=data['longitude'].dropna(),
    y=data['latitude'].dropna(),
    cmap='Blues',
    fill=True,
    bw_adjust=0.5
)
plt.title('Heatmap of Flight Locations (Sampled Data)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

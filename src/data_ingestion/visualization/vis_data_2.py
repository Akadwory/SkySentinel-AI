import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load Data ---
# Load the CSV file in chunks to prevent memory overload
chunk_size = 100000  # Adjust based on system capability
chunks = pd.read_csv('/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv', chunksize=chunk_size)
flight_data = pd.concat(chunks, ignore_index=True)

# --- Data Preparation ---
flight_data['time_position'] = pd.to_datetime(flight_data['time_position'], errors='coerce')
flight_data['last_contact'] = pd.to_datetime(flight_data['last_contact'], errors='coerce')

# --- Sampling ---
# Use a 10% sample for quicker visualization
sampled_data = flight_data.sample(frac=0.1, random_state=42)

# --- Visualization 1: Geo Altitude Distribution ---
plt.figure(figsize=(12, 6))
sns.histplot(sampled_data['geo_altitude'].dropna(), bins=50, kde=True, color='skyblue')
plt.title('Distribution of Geo Altitude (Sampled Data)')
plt.xlabel('Geo Altitude (meters)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# --- Visualization 2: Top Origin Countries ---
top_countries = sampled_data['origin_country'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(y=top_countries.index, x=top_countries.values, palette='viridis')
plt.title('Top 10 Origin Countries by Flight Count')
plt.xlabel('Number of Flights')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

# --- Visualization 3: Flight Count by Hour of Day ---
sampled_data['hour'] = sampled_data['time_position'].dt.hour
hourly_flight_count = sampled_data['hour'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.barplot(x=hourly_flight_count.index, y=hourly_flight_count.values, palette='coolwarm')
plt.title('Flight Count Distribution by Hour of Day (Sampled Data)')
plt.xlabel('Hour of Day')
plt.ylabel('Flight Count')
plt.tight_layout()
plt.show()

# --- Visualization 4: Flight Location Heatmap ---
plt.figure(figsize=(12, 6))
sns.kdeplot(x=sampled_data['longitude'], y=sampled_data['latitude'], cmap='Blues', shade=True, thresh=0.05)
plt.title('Heatmap of Flight Locations (Sampled Data)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()

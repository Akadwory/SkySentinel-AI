import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv"
df = pd.read_csv(data_path)

# Sample the data to improve performance
df_sampled = df.sample(frac=0.05, random_state=42)

# 1. **Geo Altitude Distribution Plot**
plt.figure(figsize=(12, 6))
sns.histplot(df_sampled['geo_altitude'].dropna(), bins=30, kde=True, color="skyblue")
plt.title("Distribution of Geo Altitude (Sampled Data)")
plt.xlabel("Geo Altitude (meters)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# 2. **Top 10 Origin Countries**
top_countries = df_sampled['origin_country'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis")
plt.title("Top 10 Origin Countries by Flight Count")
plt.xlabel("Number of Flights")
plt.ylabel("Country")
plt.show()

# 3. **Flight Count by Hour of Day**
df_sampled['time_position'] = pd.to_datetime(df_sampled['time_position'], errors='coerce')
df_sampled['hour_of_day'] = df_sampled['time_position'].dt.hour
hourly_counts = df_sampled['hour_of_day'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette="coolwarm")
plt.title("Flight Count Distribution by Hour of Day (Sampled Data)")
plt.xlabel("Hour of Day")
plt.ylabel("Flight Count")
plt.show()

# 4. **3D Scatter Plot (Location vs. Altitude)**
fig = px.scatter_3d(
    df_sampled,
    x='longitude',
    y='latitude',
    z='geo_altitude',
    color='origin_country',
    title="3D Scatter Plot of Flight Locations and Altitude",
    labels={'geo_altitude': 'Geo Altitude (meters)', 'latitude': 'Latitude', 'longitude': 'Longitude'},
    opacity=0.7
)
fig.update_traces(marker=dict(size=5))
fig.show()

import pandas as pd
import plotly.express as px

# Load the sampled dataset
file_path = '/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv'

# Load the CSV with sampling (10% of the dataset)
sample_fraction = 0.25  # Adjust this to control sample size
flight_data = pd.read_csv(file_path).sample(frac=sample_fraction, random_state=42)

# Sampling the data to avoid rendering issues due to size
flight_data_sampled = flight_data.sample(3000, random_state=42)

# Ensure necessary columns are present and drop rows with missing essential data
flight_data_cleaned = flight_data_sampled.dropna(subset=['latitude', 'longitude', 'geo_altitude', 'origin_country'])

# Create a 3D scatter plot for flight paths visualization
fig = px.scatter_3d(
    flight_data_cleaned,
    x='longitude',
    y='latitude',
    z='geo_altitude',
    color='origin_country',
    hover_data=['callsign', 'origin_country'],
    title='3D Flight Route Paths Visualization (Sampled Data)',
    labels={'longitude': 'Longitude', 'latitude': 'Latitude', 'geo_altitude': 'Altitude (meters)'}
)

# Display the plot
fig.show()

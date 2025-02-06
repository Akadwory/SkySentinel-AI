import pandas as pd
import plotly.express as px

# Load a sample of the flight data
file_path = '/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv'

# Load the CSV with sampling (10% of the dataset)
sample_fraction = 0.25  # Adjust this to control sample size
data = pd.read_csv(file_path).sample(frac=sample_fraction, random_state=42)


# Sample the data to make visualization manageable
sample_data = data.sample(n=5000, random_state=42)

# Check for necessary columns
required_columns = ['latitude', 'longitude', 'geo_altitude']
if not all(col in sample_data.columns for col in required_columns):
    raise ValueError(f"Missing one or more required columns: {required_columns}")

# Drop rows with missing values in the required columns
sample_data = sample_data.dropna(subset=required_columns)

# Create the 3D scatter plot
fig = px.scatter_3d(
    sample_data,
    x='longitude',
    y='latitude',
    z='geo_altitude',
    color='origin_country',
    title='3D Scatter Plot of Flight Locations and Altitude',
    labels={
        'longitude': 'Longitude',
        'latitude': 'Latitude',
        'geo_altitude': 'Geo Altitude (meters)',
        'origin_country': 'Origin Country'
    },
    opacity=0.7
)

# Show the plot
fig.show()

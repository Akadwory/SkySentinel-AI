from opensky_api import OpenSkyApi
import time
import os

def fetch_opensky_data():
    try:
        # Fetch credentials from environment variables
        username = os.getenv("OPEN_SKY_USERNAME")
        password = os.getenv("OPEN_SKY_PASSWORD")

        if not username or not password:
            raise ValueError("Environment variables for username and password are not set")

        # Initialize the OpenSky API Client
        api = OpenSkyApi(username=username, password=password)

        # Fetch real-time flight state vectors
        print("Fetching flight data from OpenSky Network...")
        states = api.get_states()

        if states and states.states:
            for s in states.states:
                print(f"Flight: {s.callsign}, Latitude: {s.latitude}, Longitude: {s.longitude}, "
                      f"Geo Altitude: {getattr(s, 'geo_altitude', 'N/A')}, "
                      f"Baro Altitude: {getattr(s, 'baro_altitude', 'N/A')}")
            print(f"Successfully fetched {len(states.states)} flights.")
        else:
            print("No flight data available.")
    except Exception as e:
        print(f"Error fetching data from OpenSky: {e}")

if __name__ == "__main__":
    # Fetch the data every 60 seconds
    while True:
        fetch_opensky_data()
        time.sleep(60)


#export OPEN_SKY_USERNAME="skyai_ai"
#export OPEN_SKY_PASSWORD="Ahmed_7777"


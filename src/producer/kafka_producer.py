import os
import sys
import time
from kafka import KafkaProducer
import json

# Dynamically set the path to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.opensky_api import OpenSkyApi  # Import OpenSkyApi after fixing the path



def fetch_flight_data(username, password):
    """
    Fetch flight data from OpenSky API.
    """
    try:
        print("Fetching flight data from OpenSky Network...")
        api = OpenSkyApi(username=username, password=password)
        states = api.get_states()

        if states and states.states:
            flight_data = []
            for s in states.states:
                # Organize data into a dictionary
                flight = {
                    "callsign": s.callsign.strip() if s.callsign else None,
                    "latitude": s.latitude,
                    "longitude": s.longitude,
                    "geo_altitude": getattr(s, 'geo_altitude', None),
                    "baro_altitude": getattr(s, 'baro_altitude', None),
                    "velocity": s.velocity,
                    "origin_country": s.origin_country,
                    "time_position": s.time_position,
                    "last_contact": s.last_contact,
                }
                flight_data.append(flight)
            print(f"Successfully fetched {len(flight_data)} flights.")
            return flight_data
        else:
            print("No flight data available.")
            return []
    except Exception as e:
        print(f"Error fetching data from OpenSky: {e}")
        return []


def produce_flight_data():
    """
    Fetch flight data and produce to Kafka topic 'flight_data'.
    """
    try:
        # Load Kafka Producer
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
        )
        print("Kafka Producer initialized.")

        # Get environment variables for OpenSky API credentials
        username = os.getenv("OPEN_SKY_USERNAME")
        password = os.getenv("OPEN_SKY_PASSWORD")

        if not username or not password:
            raise ValueError("Environment variables OPEN_SKY_USERNAME and OPEN_SKY_PASSWORD are not set!")

        # Produce flight data continuously
        while True:
            flight_data = fetch_flight_data(username, password)

            for flight in flight_data:
                # Send data to Kafka topic 'flight_data'
                producer.send("flight_data", flight)
                print(f"Produced to Kafka: {flight}")
            
            print("Waiting 60 seconds before fetching the next batch...")
            time.sleep(60)  # Fetch data every 60 seconds

    except Exception as e:
        print(f"Error in Kafka Producer: {e}")
    finally:
        producer.close()
        print("Kafka Producer closed.")


if __name__ == "__main__":
    produce_flight_data()

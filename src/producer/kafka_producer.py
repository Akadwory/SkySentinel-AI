import os
import sys
import time
from kafka import KafkaProducer
import json
import numpy as np

# Dynamically set the path to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.opensky_api_test import OpenSkyApi  # Import OpenSkyApi after fixing the path

def fetch_flight_data(username, password):
    """
    Fetch flight data from OpenSky API and include `icao24` for aircraft identification.
    """
    try:
        print("🚀 Fetching flight data from OpenSky Network...")
        api = OpenSkyApi(username=username, password=password)
        states = api.get_states()

        if states and states.states:
            flight_data = []
            for s in states.states:
                # Convert float32 to float for JSON serialization
                flight = {
                    "icao24": s.icao24,  # ✅ Added ICAO24 aircraft identifier
                    "callsign": s.callsign.strip() if s.callsign else None,
                    "latitude": float(s.latitude) if s.latitude is not None else None,
                    "longitude": float(s.longitude) if s.longitude is not None else None,
                    "geo_altitude": float(s.geo_altitude) if s.geo_altitude is not None else None,
                    "baro_altitude": float(s.baro_altitude) if s.baro_altitude is not None else None,
                    "velocity": float(s.velocity) if s.velocity is not None else None,
                    "vertical_rate": float(s.vertical_rate) if s.vertical_rate is not None else None,
                    "on_ground": bool(s.on_ground),
                    "true_track": float(s.true_track) if s.true_track is not None else None,
                    "position_source": int(s.position_source) if s.position_source is not None else None,
                    "category": int(s.category) if s.category is not None else None,
                    "origin_country": s.origin_country,
                    "time_position": s.time_position,
                    "last_contact": s.last_contact,
                }
                flight_data.append(flight)
            print(f"✅ Successfully fetched {len(flight_data)} flights.")
            return flight_data
        else:
            print("⚠️ No flight data available.")
            return []
    except Exception as e:
        print(f"❌ Error fetching data from OpenSky: {e}")
        return []


def produce_flight_data():
    """
    Fetch flight data and produce it to Kafka topic 'flight_data'.
    """
    try:
        # Load Kafka Producer
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
        )
        print("✅ Kafka Producer initialized.")

        # Get environment variables for OpenSky API credentials
        username = os.getenv("OPEN_SKY_USERNAME")
        password = os.getenv("OPEN_SKY_PASSWORD")

        if not username or not password:
            raise ValueError("⚠️ Environment variables OPEN_SKY_USERNAME and OPEN_SKY_PASSWORD are not set!")

        # Produce flight data continuously
        while True:
            flight_data = fetch_flight_data(username, password)

            for flight in flight_data:
                # Send data to Kafka topic 'flight_data'
                producer.send("flight_data", flight)
                print(f"📡 Produced to Kafka: {flight}")

            print("⏳ Waiting 60 seconds before fetching the next batch...")
            time.sleep(60)  # Fetch data every 60 seconds

    except Exception as e:
        print(f"❌ Error in Kafka Producer: {e}")
    finally:
        producer.close()
        print("✅ Kafka Producer closed.")


if __name__ == "__main__":
    produce_flight_data()

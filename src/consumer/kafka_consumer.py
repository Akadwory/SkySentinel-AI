from kafka import KafkaConsumer
import psycopg2
import json
import os

# PostgreSQL connection details
DB_NAME = "flight_data"  # Updated to use the correct database
DB_USER = "adamkadwory"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # Ensure this is set in your environment
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL")
except Exception as e:
    print("❌ Error connecting to PostgreSQL:", e)
    exit(1)

# Create Kafka consumer
consumer = KafkaConsumer(
    'flight_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📡 Kafka Consumer started. Listening for messages...")

for message in consumer:
    flight_data = message.value

    try:
        cursor.execute("""
            INSERT INTO flight_data (  -- ✅ NOW USING `flight_data`
                callsign, latitude, longitude, geo_altitude, baro_altitude, velocity, 
                vertical_rate, on_ground, true_track, position_source, category, 
                origin_country, time_position, last_contact
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s)
            )
        """, (
            flight_data.get('callsign'),
            float(flight_data.get('latitude')) if flight_data.get('latitude') is not None else None,
            float(flight_data.get('longitude')) if flight_data.get('longitude') is not None else None,
            float(flight_data.get('geo_altitude')) if flight_data.get('geo_altitude') is not None else None,
            float(flight_data.get('baro_altitude')) if flight_data.get('baro_altitude') is not None else None,
            float(flight_data.get('velocity')) if flight_data.get('velocity') is not None else None,
            float(flight_data.get('vertical_rate')) if flight_data.get('vertical_rate') is not None else None,
            bool(flight_data.get('on_ground')) if flight_data.get('on_ground') is not None else None,
            float(flight_data.get('true_track')) if flight_data.get('true_track') is not None else None,
            int(flight_data.get('position_source')) if flight_data.get('position_source') is not None else None,
            int(flight_data.get('category')) if flight_data.get('category') is not None else None,
            flight_data.get('origin_country'),
            flight_data.get('time_position'),
            flight_data.get('last_contact')
        ))
        conn.commit()
        print(f"✅ Inserted flight data: {flight_data.get('callsign')}")

    except Exception as e:
        print("❌ Error inserting data:", e)
        conn.rollback()

cursor.close()
conn.close()

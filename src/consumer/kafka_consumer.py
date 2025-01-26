from kafka import KafkaConsumer
import psycopg2
import json
import os

# PostgreSQL connection details
DB_NAME = "pstgres"
DB_USER = "adamkadwory"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # Ensure you've set this in your environment
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
    print("Connected to PostgreSQL")
except Exception as e:
    print("Error connecting to PostgreSQL:", e)
    exit(1)

# Create Kafka consumer
consumer = KafkaConsumer(
    'flight_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer started. Listening for messages...")

for message in consumer:
    flight_data = message.value
    try:
        cursor.execute("""
            INSERT INTO flight_data (
                callsign, latitude, longitude, geo_altitude, 
                baro_altitude, velocity, origin_country, 
                time_position, last_contact
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s))
        """, (
            flight_data['callsign'], flight_data['latitude'], flight_data['longitude'],
            flight_data['geo_altitude'], flight_data['baro_altitude'],
            flight_data['velocity'], flight_data['origin_country'],
            flight_data['time_position'], flight_data['last_contact']
        ))
        conn.commit()
        print(f"Inserted flight data: {flight_data['callsign']}")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()

cursor.close()
conn.close()

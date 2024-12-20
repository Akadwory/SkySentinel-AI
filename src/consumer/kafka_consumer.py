from kafka import KafkaConsumer
import json

def consume_flight_data():
    """
    Consumes flight data from the Kafka topic 'flight_data'
    and prints it to the console.
    """
    try:
        print("Starting Kafka Consumer...")

        # Initialize the Kafka consumer
        consumer = KafkaConsumer(
            'flight_data',                      # Kafka topic to consume
            bootstrap_servers='localhost:9092', # Kafka broker address
            group_id='flight_consumer_group',   # Consumer group name
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) # Deserialize JSON data
        )

        print("Connected to Kafka. Listening for messages...")

        # Continuously listen for messages on the topic
        for message in consumer:
            flight_data = message.value  # Deserialized message data
            print(f"Consumed Flight Data: {flight_data}")

    except Exception as e:
        print(f"Error consuming data: {e}")
    finally:
        print("Shutting down Kafka Consumer.")

if __name__ == "__main__":
    consume_flight_data()

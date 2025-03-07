from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)

# Kafka configuration
KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "weather-data"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id="weather-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Shared variable to store the latest weather data
latest_weather_data = None

# Function to continuously consume messages from Kafka
def consume_messages():
    global latest_weather_data
    for message in consumer:
        latest_weather_data = message.value  # Update the latest weather data

# Start Kafka consumer in a separate thread
consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

@app.route('/weather', methods=['GET'])
def get_weather():
    if latest_weather_data:
        return jsonify(latest_weather_data), 200
    else:
        return jsonify({"message": "No data available yet."}), 404

if __name__ == "__main__":
    app.run(debug=True)

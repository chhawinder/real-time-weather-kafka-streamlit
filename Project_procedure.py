from kafka import KafkaProducer
import json
import requests
import time

# Kafka Configuration
KAFKA_TOPIC = "weather-data"
KAFKA_SERVER = "localhost:9092"

# OpenWeatherMap API Configuration (replace with your API Key)
API_KEY = "You api in Double qoutes"  # Replace with your API key
CITIES = ["Delhi", "New York", "London", "Tokyo"]#can add more citis if you want 

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Function to get weather data from OpenWeatherMap
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Infinite loop to fetch and send weather data every 10 seconds for each city
while True:
    for i, city in enumerate(CITIES):
        weather_data = get_weather_data(city)
        if weather_data:
            # Send data to Kafka, assigning each city to a different partition
            # Partition is chosen by the modulo operation: 4 cities, so partition ranges from 0 to 3
            partition = i % 4  # We have 4 cities, so we assign each city to a different partition
            producer.send(KAFKA_TOPIC, value=weather_data)
            print(f"Sent weather data for {city}: {weather_data}")
        else:
            print(f"Failed to fetch weather data for {city}.")

    time.sleep(10)  # Wait for 10 seconds before fetching again

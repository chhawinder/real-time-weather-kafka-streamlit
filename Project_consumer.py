from pyspark.sql import SparkSession

# Add Kafka dependencies
spark = SparkSession.builder \
    .appName("KafkaWeatherDataProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Your Kafka reading and processing logic
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather-data") \
    .load()



from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import json

# # Create Spark session
# spark = SparkSession.builder \
#     .appName("KafkaWeatherDataProcessor") \
#     .getOrCreate()

# # Subscribe to the Kafka topic
# kafka_stream = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "weather-data") \
#     .load()

# The value column contains the weather data as a byte array, so we need to convert it
weather_data = kafka_stream.selectExpr("CAST(value AS STRING) AS weather_json")

# Parse the JSON data into columns
parsed_weather_data = weather_data.select(
    expr("json_tuple(weather_json, 'coord', 'weather', 'main') AS (coord, weather, main)"))

# Print the processed data to the console (for testing)
query = parsed_weather_data.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()  # Keep the streaming process alive

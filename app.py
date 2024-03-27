from kafka import KafkaConsumer
from pymongo import MongoClient
import json

mongo_client = MongoClient('localhost', 27017)  # Connect to your MongoDB instance
db = mongo_client["Kafka-Test"]  # Use (or create) a database
success = db["success"]
pending = db["pending"]
failed = db["failed"]

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'messagebox',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest'
)

for message in consumer:
    try:
        json_data = json.loads(message.value.decode('utf-8'))
        print(f"Received message: {json_data}")
        # Access the "message" key from the json_data dictionary

        if json_data["status"] == "SUCCESS":
            success.insert_one({
                "status": json_data["status"],
                "time": json_data["time"],
                "count": json_data["count"],
                "date": json_data["date"],
            })
        elif json_data["status"] == "FAILED":
            failed.insert_one({
                "status": json_data["status"],
                "time": json_data["time"],
                "count": json_data["count"],
                "date": json_data["date"],
            })
        elif json_data["status"] == "PENDING":
            pending.insert_one({
                "status": json_data["status"],
                "time": json_data["time"],
                "count": json_data["count"],
                "date": json_data["date"],
            })
    except json.JSONDecodeError:
        print(f"Error decoding message: {message.value}")

consumer.close()

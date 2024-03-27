import random

from kafka import KafkaProducer
from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')


@app.route("/send", methods=['POST'])
def send_message():

    statuses = ["SUCCESS", "PENDING", "FAILED"]

    for i in range(0, 10):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')

        data = {
            "status": random.choice(statuses),
            "time": current_time,
            "count": 1,
            "date": current_date
        }
        # Serialize message as JSON string before sending
        message_json = json.dumps(data)
        producer.send('messagebox', message_json.encode('utf-8'))
    return jsonify({'message': 'Message sent to Kafka'}), 200


if __name__ == "__main__":
    app.run(port=5000)

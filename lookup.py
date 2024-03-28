import json

from flask import Flask
from pymongo import MongoClient
from threading import Thread
import logging

app = Flask(__name__)

mongo_client = MongoClient('localhost', 27017)  # Connect to your MongoDB instance
db = mongo_client["Kafka-Test"]  # Use (or create) a database
pending = db["pending"]
logs = db["pending-transaction-logs"]


def watch_for_changes():
    try:
        with pending.watch() as stream:
            for change in stream:
                print("New data Entered")
                print(change)
                logs.insert_one(change['fullDocument'])
    except Exception as e:
        logging.error(f"An error occurred in watch_for_changes: {e}")


@app.route("/pending-logs")
def transaction_logs():
    results = []
    print("Called")
    data = logs.find()
    for d in data:
        print(d)
        d['_id'] = str(d['_id'])
        results.append(d)
    return results


if __name__ == '__main__':
    watch_thread = Thread(target=watch_for_changes)
    watch_thread.start()
    app.run(debug=True, port=9000)

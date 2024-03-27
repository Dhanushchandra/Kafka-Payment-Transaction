from flask import Flask
from pymongo import MongoClient
from threading import Thread
import logging




app = Flask(__name__)

mongo_client = MongoClient('localhost', 27017)  # Connect to your MongoDB instance
db = mongo_client["Kafka-Test"]  # Use (or create) a database
pending = db["pending"]


def watch_for_changes():
    try:
        with pending.watch() as stream:
            for change in stream:
                print("New data Entered")
                print(change)
    except Exception as e:
        logging.error(f"An error occurred in watch_for_changes: {e}")


if __name__ == '__main__':
    watch_thread = Thread(target=watch_for_changes)
    watch_thread.start()
    app.run(debug=True, port=9000)

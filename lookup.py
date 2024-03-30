from flask import Flask
from pymongo import MongoClient
from threading import Thread

app = Flask(__name__)

pending = None


def mongo_connection():
    global pending
    try:
        mongo = MongoClient('127.0.0.1', 30001, directConnection=True)
        db = mongo['Kafka-Test']
        pending = db['pending']
        print("DB Connected")
    except Exception as e:
        print("Error connecting")


@app.route("/pending")
def display():
    results = []
    data = pending.find()
    for d in data:
        d['_id'] = str(d['_id'])
        results.append(d)
    return results


def watch_for_changes():
    try:
        with pending.watch() as stream:
            for change in stream:
                print("New data Entered")
                print(change)
    except Exception as e:
        print("Failed to read", e)


if __name__ == '__main__':
    mongo_connection()
    thread1 = Thread(target=watch_for_changes)
    thread1.start()
    app.run(port=8001)

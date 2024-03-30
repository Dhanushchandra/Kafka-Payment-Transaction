from flask import Flask
from pymongo import MongoClient
from threading import Thread
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

pending = None


def mongo_connection():
    global pending
    try:
        mongo = MongoClient('127.0.0.1', 30003, directConnection=True)
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
                obj = change['fullDocument']
                obj["_id"] = str(obj["_id"])
                handle_connect(obj)
    except Exception as e:
        print("Failed to read", e)


@socketio.on("connect")
def handle_connect(data):
    if data is not None:
        socketio.emit("my_event", {'data': data})


if __name__ == '__main__':
    mongo_connection()
    thread1 = Thread(target=watch_for_changes)
    thread1.daemon = True
    thread1.start()
    socketio.run(app, port=8001, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)

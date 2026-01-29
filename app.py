from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import uuid
from config import settings
from datetime import datetime, timezone

app = Flask(__name__)
client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
collection = db[settings.COLLECTION]


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/webhook")
def webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event == "push":
        data = {
            "event": "push",
            "author": payload["pusher"]["name"],
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"],
        }
        collection.insert_one(data)

    elif event == "pull_request":
        action = payload["action"]
        pr = payload["pull_request"]

        if action == "opened":
            data = {
                "event": "pull_request",
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"],
            }
            collection.insert_one(data)

        elif action == "closed" and pr["merged"]:
            data = {
                "event": "merge",
                "author": pr["merged_by"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"],
            }
            collection.insert_one(data)

    return jsonify({"status": "ok"}), 200


@app.get("/events")
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    print(events)
    return jsonify(events), 200


if __name__ == "__main__":
    app.run(debug=True)

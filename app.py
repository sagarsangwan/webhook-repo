from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import uuid
from config import settings
from datetime import datetime, timezone

app = Flask(__name__)
client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
events = db[settings.COLLECTION]
print(events, db)
print(events.count_documents({}))


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/webhook")
def webhook():
    print("insidee")
    payload = request.json
    print(payload)
    if payload is None:
        return jsonify({"error": "Invalid JSON"}), 400
    event_type = request.headers.get("X-GitHub-Event")

    if event_type != "push":
        return jsonify({"status": "ignored"}), 200
    author_data = (
        payload.get("pusher") or payload.get("author") or payload.get("sender") or {}
    )
    author = author_data.get("name", "Unknown")
    ref = payload.get("ref")
    branch = ref.split("/")[-1] if ref else None
    timestamp = payload.get("head_commit", {}).get("timestamp")
    doc = {
        "request_id": str(uuid.uuid4()),
        "action": "PUSH",
        "author": author,
        "from_branch": None,
        "to_branch": branch,
        "timestamp": timestamp,
    }
    events.insert_one(doc)
    return jsonify({"revieved": True, "event": event_type, "status": "stored"}), 201


if __name__ == "__main__":
    app.run(debug=True)

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
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid JSON"}), 400
    print(payload)
    event_type = request.headers.get("X-GitHub-Event")
    doc = {
        "request_id": str(uuid.uuid4()),
        "event_type": event_type,
        "payload": payload,
        "received_at": datetime.now(timezone.utc),
    }
    events.insert_one(doc)
    return jsonify({"revieved": True, "event": event_type, "status": "stored"}), 201


if __name__ == "__main__":
    app.run(debug=True)

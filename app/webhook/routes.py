from flask import request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo
from app.webhook import webhook



@webhook.get("/")
def home():
    return render_template("index.html")


@webhook.route("/receiver", methods=["POST"])
def receiver():

    event = request.headers.get("X-GitHub-Event")
    payload = request.json
    collection = mongo.db.events
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


@webhook.get("/events")
def events():
    collection = mongo.db.events
    data = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    return jsonify(data), 200

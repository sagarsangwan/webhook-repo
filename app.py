from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
from config import settings

client = MongoClient(settings.MONGO_URI)
db = settings.DB_NAME
events = settings.COLLECTION


@app.get("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

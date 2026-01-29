from flask import Flask
import os
from app.webhook.routes import webhook
from app.extensions import mongo
from dotenv import load_dotenv

load_dotenv()


# Creating our flask app
def create_app():

    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv(
        "MONGO_URI",
    )
    mongo.init_app(app=app)

    # registering all the blueprints
    app.register_blueprint(webhook)

    return app

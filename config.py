import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION = os.getenv("COLLECTION")
    GITHUB_SECRET = os.getenv("GITHUB_SECRET")


settings = Settings()

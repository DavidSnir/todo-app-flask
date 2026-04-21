from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_database = None

def _get_db():
    global _client, _database
    if _database is None:
        _client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        _database = _client["prod"]
    return _database

def init_db(app):
    app.config["Database"] = _get_db()
    
def get_collection(name):
    return _get_db()[name]

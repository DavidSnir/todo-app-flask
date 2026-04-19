from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_database = None

def init_db(app: Flask):
    global _client, _database
    _client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    _database = _client["prod"]
    app.config["Database"] == _database
    
def get_collection(name):
    return _database[name]
    
    

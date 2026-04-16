from flask import Flask, jsonify, request
from routes import tasks_bp
from errors import error_bp
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(tasks_bp)
app.register_blueprint(error_bp)

client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
database = client["prod"]

if __name__ == "__main__":
    app.run(debug=True)
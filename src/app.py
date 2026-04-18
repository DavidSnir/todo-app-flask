from flask import Flask, jsonify, request
from src.routes.tasks import tasks_bp
from src.errors import error_bp
from src.database.manager import TaskManager
from src.database.connection import database as db


app = Flask(__name__)
app.register_blueprint(tasks_bp)
app.register_blueprint(error_bp)

task_manager = TaskManager(db_collection=db.tasks)

if __name__ == "__main__":
    app.run(debug=True)
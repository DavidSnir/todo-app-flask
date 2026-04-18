from flask import Flask, request
from src.routes.tasks import tasks_bp
from src.routes.task_lists import task_lists_bp
from src.routes.errors import error_bp
from src.database.manager import TaskManager
from src.database.connection import database as db

def create_app():

    app = Flask(__name__)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(task_lists_bp)
    app.register_blueprint(error_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
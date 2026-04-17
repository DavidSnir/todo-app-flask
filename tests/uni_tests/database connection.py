from flask import Flask, jsonify, request
from src.routes.tasks import tasks_bp
from src.errors import error_bp


app = Flask(__name__)
app.register_blueprint(tasks_bp)
app.register_blueprint(error_bp)


if __name__ == "__main__":
    app.run(debug=True)
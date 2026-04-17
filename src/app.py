from flask import Flask, jsonify, request
from routes.tasks import tasks_bp
from errors import error_bp


app = Flask(__name__)
app.register_blueprint(tasks_bp)
app.register_blueprint(error_bp)


if __name__ == "__main__":
    app.run(debug=True)
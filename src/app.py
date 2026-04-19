from flask import Flask, render_template
from src.routes.tasks import tasks_bp
from src.routes.task_lists import task_lists_bp
from src.routes.errors import error_bp
from src.database.connection import init_db

def create_app():

    app = Flask(__name__)

    init_db(app)
    
    app.register_blueprint(tasks_bp)
    app.register_blueprint(task_lists_bp)
    app.register_blueprint(error_bp)

    @app.route("/", methods=['GET'])
    def index():
        return render_template("index.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
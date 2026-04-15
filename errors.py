from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound, BadRequest

error_bp = Blueprint("errors",__name__)

@error_bp.app_errorhandler(BadRequest)
def bad_request(e):
    return jsonify({"error": str(e)}),400

@error_bp.app_errorhandler(NotFound)
def not_found(e):
    return jsonify({"error": str(e)}),404

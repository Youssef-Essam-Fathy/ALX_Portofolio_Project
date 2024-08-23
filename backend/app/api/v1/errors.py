from flask import Blueprint, render_template, jsonify

"""
Blueprint for handling various HTTP errors in a Flask application.

This module defines error handlers for common HTTP status codes.
Each handler returns a JSON response with the error message and
the appropriate HTTP status code.

Handlers:
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 405: Method not allowed
- 409: Conflict
- 422: Unprocessable entity
- 429: Too many requests
- 503: Service unavailable
- 504: Gateway timeout
- 505: HTTP version not supported
"""

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@bp.app_errorhandler(500)
def not_found_error(error):
    return jsonify({"error": "Internal server error"}), 500

@bp.app_errorhandler(400)
def not_found_error(error):
    return jsonify({"error": "Bad request"}), 400

@bp.app_errorhandler(401)
def not_found_error(error):
    return jsonify({"error": "Unauthorized"}), 401

@bp.app_errorhandler(403)
def not_found_error(error):
    return jsonify({"error": "Forbidden"}), 403

@bp.app_errorhandler(405)
def not_found_error(error):
    return jsonify({"error": "Method not allowed"}), 405

@bp.app_errorhandler(409)
def not_found_error(error):
    return jsonify({"error": "Conflict"}), 409

@bp.app_errorhandler(422)
def not_found_error(error):
    return jsonify({"error": "Unprocessable entity"}), 422

@bp.app_errorhandler(429)
def not_found_error(error):
    return jsonify({"error": "Too many requests"}), 429

@bp.app_errorhandler(503)
def not_found_error(error):
    return jsonify({"error": "Service unavailable"}), 503

@bp.app_errorhandler(504)
def not_found_error(error):
    return jsonify({"error": "Gateway timeout"}), 504

@bp.app_errorhandler(505)
def not_found_error(error):
    return jsonify({"error": "HTTP version not supported"}), 505

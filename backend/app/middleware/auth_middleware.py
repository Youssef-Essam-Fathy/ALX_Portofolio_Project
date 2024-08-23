from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

def token_required(func):
    """
    Token verification decorator.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: Decorated function that enforces token validation.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Ensure the JWT is valid
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"msg": "Invalid or missing token"}), 401
    return decorated

def setup_jwt_middleware(app):
    """
    Middleware to validate JWT tokens before processing requests.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.before_request
    def validate_token():
        # List of endpoints that don't require JWT validation
        open_endpoints = ["auth.login", "auth.register", "public.public"]

        # Skip JWT validation for open endpoints
        if request.endpoint not in open_endpoints:
            try:
                verify_jwt_in_request()  # Ensure the JWT is valid
            except Exception as e:
                return jsonify({"msg": "Invalid or missing token"}), 401

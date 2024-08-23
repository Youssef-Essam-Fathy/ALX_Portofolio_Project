from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from ..models.user import User

def role_required(required_roles, *args):
    """
    Role-based access control decorator.

    Args:
        required_roles (list): List of roles allowed to access the route.

    Returns:
        Function: Decorated function that enforces role-based access.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Ensure the JWT is valid
            current_user = get_jwt_identity()  # Get the identity from the JWT
            user = User.query.filter_by(username=current_user).first()  # Fetch user from the database

            if user is None:
                return jsonify({"error": "User not found"}), 404

            if user.role not in required_roles:
                return jsonify({"error": "Access denied"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator

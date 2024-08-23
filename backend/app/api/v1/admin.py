"""
Admin Blueprint Routes

This module defines the Flask blueprint for handling routes related to the admin interface.
It provides a simple route to welcome the admin user.

Routes:
    - /admin (GET): Displays a welcome message to users with the admin role.

Dependencies:
    - app: The Flask application instance.
    - Blueprint: Flask's blueprint class for grouping related routes.
    - role_required: Custom middleware to enforce role-based access control.
    - UserRole: Enum for user roles, used to enforce admin-only access.
"""
from flask import Blueprint, jsonify
from ...middleware.role_based_middleware import role_required
from ...models.user import UserRole

bp = Blueprint('admin', __name__)


@bp.route('/admin')
@role_required(UserRole.ADMIN)
def admin():
    """
    Admin endpoint that returns a welcome message for admin users.

    This route is accessible only to users with the ADMIN role.

    Returns:
        JSON response containing a welcome message.
    """
    return jsonify({'message': 'Welcome, admin!'})

"""
Teacher Blueprint Routes

This module defines the Flask blueprint for handling routes related to the teacher interface.
It provides a simple route to welcome the teacher user.

Routes:
    - /teacher (GET): Displays a welcome message to users with the teacher role.

Dependencies:
    - app: The Flask application instance.
    - Blueprint: Flask's blueprint class for grouping related routes.
    - role_required: Custom middleware to enforce role-based access control.
    - UserRole: Enum for user roles, used to enforce teacher-only access.
"""
from flask import Blueprint, jsonify
from ...middleware.role_based_middleware import role_required
from ...models.user import UserRole

bp = Blueprint('teacher', __name__)


@bp.route('/teacher', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER)
def teacher():
    """
    Teacher endpoint that returns a welcome message for teacher users.

    This route is accessible only to users with the TEACHER role.

    Returns:
        JSON response containing a welcome message.
    """
    return jsonify({'message': 'Welcome, teacher!'})

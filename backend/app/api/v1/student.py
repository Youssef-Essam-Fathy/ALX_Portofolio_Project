"""
Student Blueprint Routes

This module defines the Flask blueprint for handling routes related to the student interface.
It provides a simple route to welcome the student user.

Routes:
    - /student (GET): Displays a welcome message to users with the student role.

Dependencies:
    - app: The Flask application instance.
    - Blueprint: Flask's blueprint class for grouping related routes.
    - role_required: Custom middleware to enforce role-based access control.
    - UserRole: Enum for user roles, used to enforce student-only access.
"""
from flask import Blueprint, jsonify
from ...middleware.role_based_middleware import role_required
from ...models.user import UserRole

bp = Blueprint('student', __name__)


@bp.route('/student')
@role_required(UserRole.STUDENT)
def student():
    """
    Student endpoint that returns a welcome message for student users.

    This route is accessible only to users with the STUDENT role.

    Returns:
        JSON response containing a welcome message.
    """
    return jsonify({'message': 'Welcome, student!'})

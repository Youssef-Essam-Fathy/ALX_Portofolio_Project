"""
Auth Blueprint Routes

This module defines the authentication routes for the application, including
user registration, login, and logout functionality. The routes handle
requests related to user authentication and session management.

Routes:
    /register (POST):
        Registers a new user in the system. The endpoint expects a JSON payload
        containing the username, password, and an optional role (default is STUDENT).
        Returns an error if the user already exists or if the role is invalid.

    /login (POST):
        Authenticates a user based on the provided username and password. If
        successful, logs in the user and returns a JWT access token.

    /logout (GET):
        Logs out the authenticated user. This route requires a valid JWT token.

Dependencies:
    Flask:
        Blueprint, request, jsonify, render_template, redirect, url_for,
        current_app
    app.models.user:
        User, UserRole
    flask_login:
        login_user, logout_user
    flask_jwt_extended:
        create_access_token, jwt_required
    app.api.v1.users:
        create_user
    app.services.auth_service:
        send_account_created_email
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from app.models.user import User, UserRole
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, jwt_required
from app.api.v1.users import create_user
from app.services.auth_service import send_account_created_email

bp = Blueprint('auth', __name__)

@bp.route('/register', strict_slashes=False, methods=['POST'])
def register():
    """
    Register a new user in the system.

    This route handles the registration of a new user. It expects a JSON payload
    containing the username, password, and an optional role (default is STUDENT).
    The route checks if the user already exists in the database and returns an
    error if so. If the role is valid, the user is created and an account creation
    email is sent.

    Returns:
        JSON response indicating success or failure with appropriate HTTP status codes.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user:
        return jsonify({"message": f"User already exists with id: {user.id}"}), 400
    role = data.get('role', UserRole.STUDENT)
    if role not in [UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN]:
        return jsonify({"error": "Invalid role"}), 400

    with current_app.test_request_context('/users/', method='POST', json=data):
        response = create_user()

    user = User.query.filter_by(username=data.get('username')).first()

    send_account_created_email(user)
    return response

@bp.route('/login', strict_slashes=False, methods=['POST'])
def login():
    """
    Authenticate a user and provide a JWT token.

    This route handles user login by verifying the provided username and password.
    If authentication is successful, the user is logged in and a JWT access token
    is returned. The token can be used for subsequent authenticated requests.

    Returns:
        JSON response with a success message, user details, and access token on success.
        Error message with HTTP 401 status code on failure.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.verify_password(data.get('password')):
        login_user(user)
        access_token = create_access_token(identity=user.username)
        return jsonify({"message": "Logged in successfully", "user": user.to_dict(), "access_token": access_token}), 200
    return jsonify({"message": "Invalid name or password"}), 401

@bp.route('/logout', strict_slashes=False)
@jwt_required()
def logout():
    """
    Log out the authenticated user.

    This route handles user logout. It requires a valid JWT token to identify
    the user session. Once logged out, the session is terminated and a success
    message is returned.

    Returns:
        JSON response indicating successful logout.
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

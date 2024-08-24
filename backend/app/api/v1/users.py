from flask import Blueprint, jsonify, request
from ...models.user import User, UserRole
from ... import db
from ...middleware.role_based_middleware import role_required
from validator_collection import checkers

bp = Blueprint('users', __name__)

@bp.route('/users/', strict_slashes=False, methods=['POST'])
def create_user():
    """
    Create a new user.

    This route handles the creation of a new user based on the provided
    JSON data in the request body. It checks if the username already exists,
    validates the role, and creates the user if everything is valid.

    Returns:
    --------
    Response object (JSON):
        - 201: On successful creation of the user with user data.
        - 409: If the username already exists.
        - 400: If an invalid role is provided.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user is not None:
        return jsonify({"message": "User already found", "id": user.id}), 409  # conflict

    role = data.get('role', UserRole.STUDENT)
    userRole = [UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN]
    if role not in userRole:
        return jsonify({"error": "Invalid role"}), 400

    user = User(**{key: value for key, value in data.items() if key != 'password'})
    user.password = data['password']
    user.role = role
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": user.to_dict()}), 201


@bp.route('/users/', strict_slashes=False, methods=['GET'])
@role_required(UserRole.ADMIN)
def get_users():
    """
    Retrieve all users.

    This route returns a list of all users in the database.

    Returns:
    --------
    Response object (JSON):
        - 200: List of all users.
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@bp.route('/users/<int:user_id>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.ADMIN)
def get_user(user_id):
    """
    Retrieve a user by ID.

    This route retrieves a user based on the provided user ID.

    Parameters:
    -----------
    user_id : int
        The ID of the user to be retrieved.

    Returns:
    --------
    Response object (JSON):
        - 200: User data for the provided ID.
        - 404: If the user with the given ID is not found.
    """
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@bp.route('/users/<string:username>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.ADMIN)
def get_user_by_username(username):
    """
    Retrieve a user by username.

    This route retrieves a user based on the provided username.

    Parameters:
    -----------
    username : str
        The username of the user to be retrieved.

    Returns:
    --------
    Response object (JSON):
        - 200: User data for the provided username.
        - 404: If the user with the given username is not found.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@bp.route('/users/by-role/<string:role>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.ADMIN)
def get_user_by_role(role):
    """
    Retrieve users by role.

    This route retrieves all users with the specified role.

    Parameters:
    -----------
    role : str
        The role of the users to be retrieved. Valid roles are 'student',
        'teacher', and 'admin'.

    Returns:
    --------
    Response object (JSON):
        - 200: List of users with the specified role.
        - 400: If an invalid role is provided.
    """
    userRole = [UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN]
    if role not in userRole:
        return jsonify({"error": "Invalid role"}), 400

    users = User.query.filter_by(role=role).all()
    return jsonify([user.to_dict() for user in users]), 200


@bp.route('/users/<int:user_id>', strict_slashes=False, methods=['PUT'])
@role_required(UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT)
def update_user(user_id):
    """
    Update a user by ID.

    This route updates the details of a user based on the provided user ID
    and JSON data in the request body. It supports updating fields like
    username, role, and password.

    Parameters:
    -----------
    user_id : int
        The ID of the user to be updated.

    Returns:
    --------
    Response object (JSON):
        - 200: On successful update of the user with the updated data.
        - 400: If an invalid role is provided.
        - 404: If the user with the given ID is not found.
    """
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    userRole = [UserRole.STUDENT, UserRole.TEACHER, UserRole.ADMIN]

    for key, value in data.items():
        if key == 'password':
            user.password(value)
        elif key == 'role':
            if value in userRole:
                user.role = value
            else:
                return jsonify({"error": "Invalid role"}), 400
        elif hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200


@bp.route('/users/<int:user_id>', strict_slashes=False, methods=['DELETE'])
@role_required(UserRole.ADMIN)
def delete_user(user_id):
    """
    Delete a user by ID.

    This route deletes a user based on the provided user ID.

    Parameters:
    -----------
    user_id : int
        The ID of the user to be deleted.

    Returns:
    --------
    Response object (JSON):
        - 200: On successful deletion of the user.
        - 404: If the user with the given ID is not found.
    """
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

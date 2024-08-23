"""
Content Blueprint Routes

This module handles the creation, retrieval, updating, and deletion (CRUD)
of courses and lessons within the application. The routes defined here manage
content-related operations that require specific user roles, such as teachers
and administrators.

Routes:
    /courses (POST):
        Creates a new course. Only accessible to users with the TEACHER role.
    /courses (GET):
        Retrieves all available courses.
    /courses/<int:course_id> (GET):
        Retrieves details of a specific course by its ID.
    /courses/<int:course_id> (PUT):
        Updates an existing course. Only the course's author can perform this action.
    /courses/<int:course_id> (DELETE):
        Deletes a course. Only the course's author can perform this action.

    /lessons (POST):
        Creates a new lesson. Only accessible to users with the TEACHER role.
    /lessons (GET):
        Retrieves all lessons, with optional pagination.
    /lessons/<int:lesson_id> (GET):
        Retrieves details of a specific lesson by its ID.
    /lessons/<int:lesson_id> (PUT):
        Updates an existing lesson. Only the lesson's author can perform this action.
    /lessons/<int:lesson_id> (DELETE):
        Deletes a lesson. Only the lesson's author can perform this action.

    /courses/<int:course_id>/lessons (GET):
        Retrieves all lessons associated with a specific course.
    /lessons/<int:lesson_id>/course (GET):
        Retrieves the course associated with a specific lesson.
    /lessons/<int:lesson_id>/author (GET):
        Retrieves the author of a specific lesson.
    /courses/<int:course_id>/author (GET):
        Retrieves the author of a specific course.
    /lessons/by-author/<string:author> (GET):
        Retrieves all lessons authored by a specific user.
    /courses/by-author/<string:author> (GET):
        Retrieves all courses authored by a specific user.

Dependencies:
    Flask:
        Blueprint, jsonify, request
    flask_jwt_extended:
        jwt_required, get_jwt_identity
    app.models.user:
        User, UserRole
    app.models.content:
        Course, Lesson
    app.middleware.role_based_middleware:
        role_required
    app:
        db
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, UserRole
from app.models.content import Course, Lesson
from app.middleware.role_based_middleware import role_required
from app import db

bp = Blueprint('content', __name__)

# Course CRUD operations
@bp.route('/courses', strict_slashes=False, methods=['POST'])
@role_required(UserRole.TEACHER)
def create_course():
    """
    Create a new course.

    This route allows users with the TEACHER role to create a new course. It requires
    a JSON payload with a title and description. The course's title must be unique.

    Returns:
        JSON response with the created course's details or an error message.
    """
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Missing required fields"}), 400

    if Course.query.filter_by(title=title).first():
        return jsonify({"error": "Course title already exists"}), 409

    course = Course(title=title, description=description, author_id=User.query.filter_by(username=get_jwt_identity()).first().id)
    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201

@bp.route('/courses', strict_slashes=False, methods=['GET'])
def get_courses():
    """
    Retrieve all courses.

    This route retrieves a list of all available courses.

    Returns:
        JSON response with a list of all courses.
    """
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@bp.route('/courses/<int:course_id>', strict_slashes=False, methods=['GET'])
def get_course(course_id):
    """
    Retrieve a specific course by its ID.

    This route retrieves the details of a course identified by its ID.

    Args:
        course_id (int): The ID of the course.

    Returns:
        JSON response with the course's details or a 404 error if not found.
    """
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200

@bp.route('/courses/<int:course_id>', strict_slashes=False, methods=['PUT'])
@role_required(UserRole.TEACHER)
def update_course(course_id):
    """
    Update an existing course.

    This route allows the course's author (a user with the TEACHER role) to update
    the course's title and description. The new title must be unique.

    Args:
        course_id (int): The ID of the course to update.

    Returns:
        JSON response with the updated course's details or an error message.
    """
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    data = request.get_json()

    if course.author.username != get_jwt_identity():
        return jsonify({"error": "You are not allowed to update this course"}), 403

    if data.get('title'):
        if Course.query.filter_by(title=data.get('title')).first() and Course.query.filter_by(title=data.get('title')).first().id != course_id:
            return jsonify({"error": "Course title already exists"}), 409
        course.title = data.get('title')

    if data.get('description'):
        course.description = data.get('description')

    db.session.commit()

    return jsonify(course.to_dict()), 200

@bp.route('/courses/<int:course_id>', strict_slashes=False, methods=['DELETE'])
@role_required(UserRole.TEACHER)
def delete_course(course_id):
    """
    Delete a course.

    This route allows the course's author (a user with the TEACHER role) to delete
    the course. Once deleted, the course is removed from the database.

    Args:
        course_id (int): The ID of the course to delete.

    Returns:
        JSON response indicating successful deletion or an error message.
    """
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    if course.author.username != get_jwt_identity():
        return jsonify({"error": "You are not allowed to delete this course"}), 403
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully"}), 200

# Lesson CRUD operations
@bp.route('/lessons', strict_slashes=False, methods=['POST'])
@role_required(UserRole.TEACHER)
def create_lesson():
    """
    Create a new lesson.

    This route allows users with the TEACHER role to create a new lesson. It requires
    a JSON payload with a title, body, and course_id. The lesson's title must be unique.

    Returns:
        JSON response with the created lesson's details or an error message.
    """
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    course_id = data.get('course_id')

    if not title or not body or not course_id:
        return jsonify({"error": "Missing required fields"}), 400

    if not db.session.get(Course, course_id):
        return jsonify({"error": "Invalid course_id"}), 400

    lesson = Lesson.query.filter_by(title=title).first()
    if lesson:
        return jsonify({"error": "Lesson title already exists"}), 409

    lesson = Lesson(title=title, body=body, author_id=User.query.filter_by(username=get_jwt_identity()).first().id, course_id=course_id)

    try:
        db.session.add(lesson)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(lesson.to_dict()), 201

@bp.route('/lessons', methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN)
def get_lessons():
    """
    Retrieve all lessons with pagination.

    This route retrieves a list of all lessons, with optional pagination.

    Returns:
        JSON response with a list of lessons, including pagination details.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    lessons_query = Lesson.query.order_by(Lesson.created_at.desc())
    paginated_lessons = lessons_query.paginate(page=page, per_page=per_page, error_out=False)

    lessons = [lesson.to_dict() for lesson in paginated_lessons.items]
    result = {
        'items': lessons,
        'total': paginated_lessons.total,
        'page': paginated_lessons.page,
        'pages': paginated_lessons.pages,
    }

    return jsonify(result), 200

@bp.route('/lessons/<int:lesson_id>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN)
def get_lesson(lesson_id):
    """
    Retrieve a specific lesson by its ID.

    This route retrieves the details of a lesson identified by its ID.

    Args:
        lesson_id (int): The ID of the lesson.

    Returns:
        JSON response with the lesson's details or a 404 error if not found.
    """
    lesson =db.session.get(Lesson, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson.to_dict()), 200

@bp.route('/lessons/<int:lesson_id>', strict_slashes=False, methods=['PUT'])
@role_required(UserRole.TEACHER)
def update_lesson(lesson_id):
    """
    Update an existing lesson.

    This route allows the lesson's author (a user with the TEACHER role) to update
    the lesson's title, body, and course_id.

    Args:
        lesson_id (int): The ID of the lesson to update.

    Returns:
        JSON response with the updated lesson's details or an error message.
    """
    lesson =db.session.get(Lesson, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404
    data = request.get_json()

    if lesson.author.username != get_jwt_identity():
        return jsonify({"error": "You are not allowed to update this lesson"}), 403

    if data.get('title'):
        lesson.title = data.get('title')
    if data.get('body'):
        lesson.body = data.get('body')
    if data.get('course_id'):
        if not Course.query.get(data.get('course_id')):
            return jsonify({"error": "Invalid course_id"}), 400
        lesson.course_id = data.get('course_id')

    db.session.commit()

    return jsonify(lesson.to_dict()), 200

@bp.route('/lessons/<int:lesson_id>', strict_slashes=False, methods=['DELETE'])
@role_required(UserRole.TEACHER)
def delete_lesson(lesson_id):
    """
    Delete a lesson.

    This route allows the lesson's author (a user with the TEACHER role) to delete
    the lesson. Once deleted, the lesson is removed from the database.

    Args:
        lesson_id (int): The ID of the lesson to delete.

    Returns:
        JSON response indicating successful deletion or an error message.
    """
    lesson =db.session.get(Lesson, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404
    if lesson.author.username != get_jwt_identity():
        return jsonify({"error": "You are not allowed to delete this lesson"}), 403
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson deleted successfully"}), 200

# Get lessons by course
@bp.route('/courses/<int:course_id>/lessons', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_lessons_by_course(course_id):
    """
    Retrieve all lessons associated with a specific course.

    This route retrieves all lessons that belong to a course identified by its ID.

    Args:
        course_id (int): The ID of the course.

    Returns:
        JSON response with a list of lessons for the specified course.
    """
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    return jsonify([lesson.to_dict() for lesson in lessons]), 200

# Get course by lesson
@bp.route('/lessons/<int:lesson_id>/course', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_course_by_lesson(lesson_id):
    """
    Retrieve the course associated with a specific lesson.

    This route retrieves the course details for the course to which a specific
    lesson belongs.

    Args:
        lesson_id (int): The ID of the lesson.

    Returns:
        JSON response with the course's details.
    """
    lesson =db.session.get(Lesson, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson.course.to_dict()), 200

# Get author by lesson
@bp.route('/lessons/<int:lesson_id>/author', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_author_by_lesson(lesson_id):
    """
    Retrieve the author of a specific lesson.

    This route retrieves the user details of the author who created a specific lesson.

    Args:
        lesson_id (int): The ID of the lesson.

    Returns:
        JSON response with the author's details.
    """
    lesson =db.session.get(Lesson, lesson_id)
    if lesson is None:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson.author.to_dict()), 200

# Get author by course
@bp.route('/courses/<int:course_id>/author', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_author_by_course(course_id):
    """
    Retrieve the author of a specific course.

    This route retrieves the user details of the author who created a specific course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        JSON response with the author's details.
    """
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.author.to_dict()), 200

# Get lessons by author
@bp.route('/lessons/by-author/<string:author>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_lessons_by_author(author):
    """
    Retrieve all lessons authored by a specific user.

    This route retrieves all lessons created by a specific author, identified by
    their username.

    Args:
        author (str): The username of the author.

    Returns:
        JSON response with a list of lessons authored by the specified user.
    """
    lessons = Lesson.query.join(User).filter(User.username == author).all()
    return jsonify([lesson.to_dict() for lesson in lessons]), 200

# Get courses by author
@bp.route('/courses/by-author/<string:author>', strict_slashes=False, methods=['GET'])
@role_required(UserRole.TEACHER, UserRole.ADMIN, UserRole.STUDENT)
def get_courses_by_author(author):
    """
    Retrieve all courses authored by a specific user.

    This route retrieves all courses created by a specific author, identified by
    their username.

    Args:
        author (str): The username of the author.

    Returns:
        JSON response with a list of courses authored by the specified user.
    """
    courses = Course.query.join(User).filter(User.username == author).all()
    return jsonify([course.to_dict() for course in courses]), 200

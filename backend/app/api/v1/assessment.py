"""
Content Blueprint Routes

This module defines the Flask blueprint for handling assessment-related routes
in the application. It provides CRUD operations for assessments, along with
routes for submitting and retrieving submissions, and accessing assessments
based on user roles.

Routes:
    - /assessment (POST): Create a new assessment (Teacher only).
    - /assessment (GET): Retrieve all assessments (Teacher and Student).
    - /assessment/<int:assessment_id> (GET): Retrieve a specific assessment by ID (Teacher and Student).
    - /assessment/<int:assessment_id> (PUT): Update an existing assessment (Teacher only).
    - /assessment/<int:assessment_id> (DELETE): Delete an assessment (Teacher only).
    - /assessment/user (GET): Retrieve all assessments created by the current user (Teacher and Student).
    - /assessment/user/<int:assessment_id> (GET): Retrieve a specific assessment created by the current user (Teacher and Student).
    - /assessment/lesson/<int:lesson_id> (GET): Retrieve all assessments for a specific lesson (Teacher and Student).
    - /assessment/course/<int:course_id> (GET): Retrieve all assessments for a specific course (Teacher and Student).
    - /assessment/user/course/<int:course_id> (GET): Retrieve all assessments created by the current user for a specific course (Teacher and Student).
    - /assessment/user/lesson/<int:lesson_id> (GET): Retrieve all assessments created by the current user for a specific lesson (Teacher and Student).
    - /assessment/<int:assessment_id>/submit (POST): Submit an assessment (Student only).
    - /assessment/<int:assessment_id>/submissions (GET): Retrieve all submissions for a specific assessment (Teacher only).
    - /assessment/<int:assessment_id>/my-submission (GET): Retrieve the current user's submission for a specific assessment (Student only).

Dependencies:
    - app: The Flask application instance.
    - Blueprint: Flask's blueprint class for grouping related routes.
    - role_required: Custom middleware to enforce role-based access control.
    - jwt_required: JWT authentication decorator.
    - get_jwt_identity: Function to retrieve the identity of the currently authenticated user.
    - User, Assessment, Submission: ORM models representing the user, assessment, and submission entities.
    - db: SQLAlchemy database instance for interacting with the database.
    - datetime: Python's datetime module for handling date and time operations.
    - json: Python's JSON module for parsing and generating JSON.
"""
from flask import Blueprint, render_template, request, jsonify
from ...models.assessment import Assessment
from ...middleware.role_based_middleware import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models.user import User
from ...models.submission import Submission
from ... import db
from datetime import datetime
import json

bp = Blueprint('assessment', __name__)

# CRUD operations for Assessment Model

@bp.route('/assessment', methods=['POST'])
@role_required('teacher')
def create_assessment():
    """
    Create a new assessment.

    This route allows a teacher to create a new assessment, including its title,
    lesson_id, course_id, questions, type, and answers. The assessment must have
    a unique title and all necessary fields must be provided.

    Returns:
        JSON response with the created assessment details or an error message.
    """
    username = get_jwt_identity()
    data = request.get_json()

    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    if 'lesson_id' not in data:
        return jsonify({"error": "lesson_id is required"}), 400

    if 'type' not in data or data['type'] is None:
        return jsonify({"error": "type is required and cannot be null"}), 400

    assessment = Assessment.query.filter_by(title=data["title"]).first()
    if assessment is not None:
        return jsonify({"message": "Assessment already found", "id": assessment.id}), 409  # Conflict

    questions_json = json.dumps(data['questions'])
    answers_json = json.dumps(data['answers'])

    assessment = Assessment(
        title=data['title'],
        lesson_id=data['lesson_id'],
        course_id=data['course_id'],
        questions=questions_json,
        type=data['type'],
        answers=answers_json
    )

    user = User.query.filter_by(username=username).first()
    assessment.author_id = user.id
    assessment.author = user

    db.session.add(assessment)
    db.session.commit()

    return jsonify({"message": "Assessment created successfully", "assessment": assessment.to_dict()}), 201

@bp.route('/assessment', methods=['GET'])
@role_required('teacher', 'student')
def get_assessments():
    """
    Retrieve all assessments.

    This route allows teachers and students to retrieve all available assessments.

    Returns:
        JSON response with a list of assessments.
    """
    assessments = Assessment.query.all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

@bp.route('/assessment/<int:assessment_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_assessment(assessment_id):
    """
    Retrieve a specific assessment by ID.

    This route allows teachers and students to retrieve a specific assessment
    using its ID.

    Args:
        assessment_id (int): The ID of the assessment to retrieve.

    Returns:
        JSON response with the assessment's details or an error message.
    """
    assessment = db.session.get(Assessment, assessment_id)
    return jsonify(assessment.to_dict()), 200

@bp.route('/assessment/<int:assessment_id>', methods=['PUT'])
@role_required('teacher')
def update_assessment(assessment_id):
    """
    Update an existing assessment.

    This route allows a teacher to update the title, questions, and answers of an
    existing assessment.

    Args:
        assessment_id (int): The ID of the assessment to update.

    Returns:
        JSON response with the updated assessment's details or an error message.
    """
    assessment = db.session.get(Assessment, assessment_id)
    data = request.get_json()
    if data.get('title'):
        assessment.title = data.get('title')
    if data.get('questions'):
        assessment.questions = json.dumps(data.get('questions'))
    if data.get('answers'):
        assessment.answers = json.dumps(data.get('answers'))
    db.session.commit()
    return jsonify(assessment.to_dict()), 200

@bp.route('/assessment/<int:assessment_id>', methods=['DELETE'])
@role_required('teacher')
def delete_assessment(assessment_id):
    """
    Delete an assessment.

    This route allows a teacher to delete an existing assessment from the database.

    Args:
        assessment_id (int): The ID of the assessment to delete.

    Returns:
        JSON response indicating successful deletion or an error message.
    """
    assessment = db.session.get(Assessment, assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    return jsonify({"message": "Assessment deleted successfully"}), 200

# Get all assessments created by a user
@bp.route('/assessment/user', methods=['GET'])
@role_required('teacher', 'student')
def get_user_assessments():
    """
    Retrieve all assessments created by the current user.

    This route allows teachers and students to retrieve all assessments they
    have created.

    Returns:
        JSON response with a list of assessments created by the current user.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    assessments = Assessment.query.filter_by(author_id=user.id).all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

# Get a specific user assessment by ID
@bp.route('/assessment/user/<int:assessment_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_user_assessment(assessment_id):
    """
    Retrieve a specific assessment created by the current user.

    This route allows teachers and students to retrieve a specific assessment they
    have created, using the assessment ID.

    Args:
        assessment_id (int): The ID of the assessment to retrieve.

    Returns:
        JSON response with the assessment's details or an error message.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    assessment = Assessment.query.filter_by(author_id=user.id, id=assessment_id).first()
    if assessment is None:
        return jsonify({"error": "Assessment not found"}), 404
    return jsonify(assessment.to_dict()), 200

# Get all assessments for a specific lesson
@bp.route('/assessment/lesson/<int:lesson_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_lesson_assessments(lesson_id):
    """
    Retrieve all assessments for a specific lesson.

    This route allows teachers and students to retrieve all assessments associated
    with a particular lesson.

    Args:
        lesson_id (int): The ID of the lesson.

    Returns:
        JSON response with a list of assessments for the specified lesson.
    """
    assessments = Assessment.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

# Get all assessments for a specific course
@bp.route('/assessment/course/<int:course_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_course_assessments(course_id):
    """
    Retrieve all assessments for a specific course.

    This route allows teachers and students to retrieve all assessments associated
    with a particular course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        JSON response with a list of assessments for the specified course.
    """
    assessments = Assessment.query.filter_by(course_id=course_id).all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

# Get all assessments for a user in a specific course
@bp.route('/assessment/user/course/<int:course_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_user_course_assessments(course_id):
    """
    Retrieve all assessments created by the current user for a specific course.

    This route allows teachers and students to retrieve all assessments they have
    created within a particular course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        JSON response with a list of assessments created by the current user
        within the specified course.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    assessments = Assessment.query.filter_by(course_id=course_id, author_id=user.id).all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

# Get all assessments for a user in a specific lesson
@bp.route('/assessment/user/lesson/<int:lesson_id>', methods=['GET'])
@role_required('teacher', 'student')
def get_user_lesson_assessments(lesson_id):
    """
    Retrieve all assessments created by the current user for a specific lesson.

    This route allows teachers and students to retrieve all assessments they have
    created within a particular lesson.

    Args:
        lesson_id (int): The ID of the lesson.

    Returns:
        JSON response with a list of assessments created by the current user
        within the specified lesson.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    assessments = Assessment.query.filter_by(lesson_id=lesson_id, author_id=user.id).all()
    return jsonify([assessment.to_dict() for assessment in assessments]), 200

def validate_and_score_answers(assessment, submitted_answers):
    """
    Validate and score submitted answers for an assessment.

    This function compares the submitted answers with the correct answers for
    multiple choice and true/false questions. Text answers are flagged for
    manual review by the teacher.

    Args:
        assessment (Assessment): The assessment object containing the correct answers.
        submitted_answers (list): A list of answers submitted by the student.

    Returns:
        tuple: A tuple containing the score, feedback, and a boolean indicating if
               manual grading is needed.
    """
    questions = json.loads(assessment.questions)
    score = 0
    feedback = []
    text_questions_needing_review = 0

    if len(submitted_answers) != len(questions):
        return 0, ["Number of submitted answers does not match number of questions"]

    for index, (question, submitted_answer) in enumerate(zip(questions, submitted_answers)):
        question_type = question.get('type')

        if question_type in ['multiple_choice', 'true_false']:
            correct_answer = question.get('correct_answer')
            if submitted_answer == correct_answer:
                score += 1
                feedback.append(f"Question {index + 1}: Correct (+1)")
            else:
                score -= 1
                feedback.append(f"Question {index + 1}: Incorrect (-1)")
        elif question_type == 'text':
            text_questions_needing_review += 1
            feedback.append(f"Question {index + 1}: Text answer submitted; will be graded by the teacher.")
        else:
            feedback.append(f"Question {index + 1}: Unknown question type")

    if text_questions_needing_review > 0:
        feedback.append(f"{text_questions_needing_review} text question(s) need manual review.")

    return score, feedback, text_questions_needing_review > 0

@bp.route('/assessment/<int:assessment_id>/submit', methods=['POST'])
@role_required('student')
def submit_assessment(assessment_id):
    """
    Submit an assessment.

    This route allows a student to submit answers for an assessment. If the
    student has already submitted the assessment, they cannot submit again.

    Args:
        assessment_id (int): The ID of the assessment being submitted.

    Returns:
        JSON response with the submission details, score, and feedback, or an error message.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    assessment = db.session.get(Assessment, assessment_id)
    if assessment is None:
        return jsonify({"error": "Assessment not found"}), 404

    existing_submission = Submission.query.filter_by(student_id=user.id, assessment_id=assessment_id).first()
    if existing_submission:
        return jsonify({"error": "You have already submitted this assessment."}), 400

    data = request.get_json()
    submitted_answers = data.get('answers')

    if not submitted_answers or not isinstance(submitted_answers, list):
        return jsonify({"error": "Invalid answers format"}), 400

    score, feedback, needs_manual_grading = validate_and_score_answers(assessment, submitted_answers)

    submission = Submission(
        student_id=user.id,
        assessment_id=assessment_id,
        answers=json.dumps(submitted_answers),
        feedback=json.dumps(feedback),
        submitted_at=datetime.utcnow()
    )

    db.session.add(submission)
    db.session.commit()

    response_message = "Assessment submitted successfully. "
    if needs_manual_grading:
        response_message += "Your grade will be available after the teacher has graded your submission."

    return jsonify({
        "message": response_message,
        "submission": submission.to_dict()
    }), 201

# Get submissions for an assessment (teacher only)
@bp.route('/assessment/<int:assessment_id>/submissions', methods=['GET'])
@role_required('teacher')
def get_assessment_submissions(assessment_id):
    """
    Retrieve all submissions for a specific assessment.

    This route allows a teacher to view all student submissions for a specific
    assessment.

    Args:
        assessment_id (int): The ID of the assessment.

    Returns:
        JSON response with a list of submissions for the specified assessment.
    """
    assessment = db.session.get(Assessment, assessment_id)
    if assessment is None:
        return jsonify({"error": "Assessment not found"}), 404
    submissions = Submission.query.filter_by(assessment_id=assessment_id).all()
    return jsonify({"submissions": [ submission.to_dict() for submission in submissions]}), 200

# Get the current user's submission for a specific assessment
@bp.route('/assessment/<int:assessment_id>/my-submission', methods=['GET'])
@role_required('student')
def get_user_submission(assessment_id):
    """
    Retrieve the current user's submission for a specific assessment.

    This route allows a student to view their own submission for a specific
    assessment.

    Args:
        assessment_id (int): The ID of the assessment.

    Returns:
        JSON response with the student's submission details or an error message.
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    submission = Submission.query.filter_by(assessment_id=assessment_id, student_id=user.id).first()
    if not submission:
        return jsonify({"error": "No submission found"}), 404
    return jsonify({"submission": submission.to_dict()}), 200

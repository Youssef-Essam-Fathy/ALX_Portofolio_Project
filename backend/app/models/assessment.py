from .. import db
from datetime import datetime
import json


class Assessment(db.Model):
    """Model representing an assessment in a lesson.

    Attributes:
        id (int): The assessment's ID.
        title (str): The assessment's title (unique).
        author_id (int): The ID of the user who created the assessment.
        lesson_id (int): The ID of the lesson to which the assessment belongs.
        course_id (int): The ID of the course to which the lesson belongs.
        questions (str): The assessment's questions stored as a JSON string.
        type (str): The type of assessment.
        answers (str): The assessment's answers stored as a JSON string.
        created_at (datetime): The time when the assessment was created.
        updated_at (datetime): The last time the assessment's information was updated.

    Relationships:
        course: Relationship to the Course model.
        lesson: Relationship to the Lesson model.
        author: Relationship to the User model.
    """

    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    questions = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    answers = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow)
    updated_at = db.Column(db.DATETIME, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='assessments')
    lesson = db.relationship('Lesson', back_populates='assessments')
    author = db.relationship('User', back_populates='assessments')
    submissions = db.relationship('Submission', back_populates='assessment')


    def to_dict(self):
        """Convert the Assessment object to a dictionary.

        Returns:
            dict: A dictionary representation of the assessment.
        """
        assessment_info = {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'author_id': self.author_id,
            'lesson_id': self.lesson_id,
            'course_id': self.course_id,
            'questions': json.loads(self.questions),
            'answers': json.loads(self.answers),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'author': {
                'username': self.author.username,
            },
            'lesson': {
                'title': self.lesson.title,
            },
            'course': {
                'title': self.course.title,
            }
        }
        return assessment_info

    def __repr__(self):
        """Return a string representation of the Assessment object."""
        return f'assessment {self.title} has id {self.id}'

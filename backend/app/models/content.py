from .. import db
from datetime import datetime

class Course(db.Model):
    """Model representing a course in the system.

    Attributes:
        id (int): The course's ID.
        title (str): The course's title (unique).
        description (str): The course's description.
        author_id (int): The ID of the user who created the course.
        created_at (datetime): The time when the course was created.
        updated_at (datetime): The last time the course's information was updated.

    Relationships:
        author: Relationship to the User model.
        lessons: Relationship to the Lesson model.
        assessments: Relationship to the Assessment model.
    """

    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow)
    updated_at = db.Column(db.DATETIME, onupdate=datetime.utcnow)

    # Relationships
    author = db.relationship('User', back_populates='course')
    lessons = db.relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', back_populates='course', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert the Course object to a dictionary.

        Returns:
            dict: A dictionary representation of the course.
        """
        course_info = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'author_id': self.author_id,
            'author': {
                'username': self.author.username,
            },
            'lessons': [lesson.id for lesson in self.lessons],
            'assessments': [assessment.id for assessment in self.assessments]
        }
        return course_info

    def __repr__(self):
        """Return a string representation of the Course object."""
        return f'course {self.title} has id {self.id}'


class Lesson(db.Model):
    """Model representing a lesson in a course.

    Attributes:
        id (int): The lesson's ID.
        title (str): The lesson's title (unique).
        body (str): The content of the lesson.
        author_id (int): The ID of the user who created the lesson.
        course_id (int): The ID of the course to which the lesson belongs.
        created_at (datetime): The time when the lesson was created.
        updated_at (datetime): The last time the lesson's information was updated.

    Relationships:
        course: Relationship to the Course model.
        author: Relationship to the User model.
        assessments: Relationship to the Assessment model.
    """

    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow)
    updated_at = db.Column(db.DATETIME, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='lessons')
    author = db.relationship('User', back_populates='lessons')
    assessments = db.relationship('Assessment', back_populates='lesson', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert the Lesson object to a dictionary.

        Returns:
            dict: A dictionary representation of the lesson.
        """
        lessons_info = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'author_id': self.author_id,
            'course_id': self.course_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'author': self.author.username,
            'course': self.course.title,
            'assessments': [assessment.id for assessment in self.assessments]
        }
        return lessons_info

    def __repr__(self):
        """Return a string representation of the Lesson object."""
        return (f'lesson {self.title} has id {self.id}, '
                f'author {self.author_id} and course {self.course_id}')

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import db

class UserRole:
    """Class containing constants for different user roles."""
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    """Model representing a user in the system.

    Attributes:
        id (int): The user's ID.
        firstName (str): The user's first name.
        lastName (str): The user's last name.
        age (int): The user's age.
        country (str): The user's country.
        email (str): The user's email address (unique).
        username (str): The user's username (unique).
        role (str): The user's role in the system.
        password_hash (str): The hashed password of the user.
        created_at (datetime): The time when the user was created.
        updated_at (datetime): The last time the user's information was updated.

    Relationships:
        course: Relationship to the Course model.
        lessons: Relationship to the Lesson model.
        assessments: Relationship to the Assessment model.
        submissions: Relationship to the Submission model.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    age = db.Column(db.Integer)
    country = db.Column(db.String(64))
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role = db.Column(db.String(64), index=True, nullable=False, default=UserRole.STUDENT)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='author', cascade='all, delete-orphan')
    lessons = db.relationship('Lesson', back_populates='author', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', back_populates='author')
    submissions = db.relationship('Submission', back_populates='student')

    @property  # type: ignore
    def password(self):
        """Prevent reading the password attribute."""
        raise AttributeError('password is not a readable attribute')  # type: ignore

    @password.setter
    def password(self, password):
        """Hash the password and set it to the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if the provided password matches the stored hash.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert the User object to a dictionary.

        Returns:
            dict: A dictionary representation of the user.
        """
        user_dict = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'age': self.age,
            'country': self.country,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'course': [course.to_dict() for course in self.course],
            'lessons': [lesson.to_dict() for lesson in self.lessons],
            'assessments': [assessment.to_dict() for assessment in self.assessments],
            'submissions': [submission.to_dict() for submission in self.submissions],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return user_dict

    def __repr__(self):
        """Return a string representation of the User object."""
        return (f"user {self.username} has id: {self.id} "
                f"and email: {self.email} and its role is {self.role}")

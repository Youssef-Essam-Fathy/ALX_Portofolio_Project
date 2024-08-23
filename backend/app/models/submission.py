from .. import db
from datetime import datetime

class Submission(db.Model):
    """
    Submission Model

    Represents a submission of an assessment by a student.

    Attributes:
        id (int): Primary key.
        student_id (int): Foreign key referencing the user (student) who made the submission.
        assessment_id (int): Foreign key referencing the assessment.
        answers (str): The student's answers in JSON format or as text.
        feedback (str): Feedback provided by the teacher (optional).
        submitted_at (datetime): The time when the submission was made.
        updated_at (datetime): The last time the submission's information was updated.

    Relationships:
        student: Relationship to the User model (student).
        assessment: Relationship to the Assessment model.
    """

    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', back_populates='submissions')
    assessment = db.relationship('Assessment', back_populates='submissions')

    def to_dict(self):
        """Convert the Submission object to a dictionary.

        Returns:
            dict: A dictionary representation of the submission.
        """
        submission_info = {
            'id': self.id,
            'student_id': self.student_id,
            'student': self.student.username,  # Assuming User model has a username field
            'assessment_id': self.assessment_id,
            'assessment_title': self.assessment.title,
            'answers': self.answers,
            'feedback': self.feedback,
            'submitted_at': self.submitted_at,
            'updated_at': self.updated_at
        }
        return submission_info

    def __repr__(self):
        """Return a string representation of the Submission object."""
        return f'Submission {self.id} by student {self.student_id} for assessment {self.assessment_id}'

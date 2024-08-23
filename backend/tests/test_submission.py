import unittest
from unittest.mock import patch
import json  # Use the standard library's json module
from flask import json as flask_json
from app import create_app, db
from app.models.user import User, UserRole
from app.models.content import Course, Lesson
from app.models.submission import Submission
from app.models.assessment import Assessment
from datetime import datetime

class TestSubmission(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        self.teacher = User(
            username='teacher',
            email='teacher@gmail.com',
            password='teacher',
            role=UserRole.TEACHER,
            firstName='John',
            lastName='Doe',
            age=30,
            country='USA'
        )

        self.student = User(username='student', email='student@gmail.com', password='student', role=UserRole.STUDENT)
        db.session.add(self.teacher)
        db.session.add(self.student)
        db.session.commit()

        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps({'username': 'teacher', 'password': 'teacher'}),
                                         content_type='application/json')
        self.teacher_token = json.loads(self.response.get_data(as_text=True))['access_token']

        self.response = self.client.post('/api/v1/auth/login',
                                         data=json.dumps({'username': 'student', 'password': 'student'}),
                                         content_type='application/json')
        self.student_token = json.loads(self.response.get_data(as_text=True))['access_token']

        self.course = Course(title='Test Course', description='Test Description', author_id=self.teacher.id)
        db.session.add(self.course)
        db.session.commit()

        self.lesson = Lesson(title='Test Lesson', body='Test Description', course_id=self.course.id, author_id=self.teacher.id)
        db.session.add(self.lesson)
        db.session.commit()

        self.data = {
            "title": "Sample Assessment",
            "lesson_id": 1,
            "course_id": 1,
            "type": "quiz",
            "questions": [
                {
                "question": "What is 2+2?",
                "type": "multiple_choice",
                "options": ["3", "4", "5"],
                "correct_answer": "4"
                },
                {
                "question": "Explain the theory of relativity.",
                "type": "text"
                }
            ],
            "answers": ["4", ""]
        }
        self.answers = {
            "answers": ["4", ""]
        }


        self.response = self.client.post('/api/v1/content/assessment',
                                         data=json.dumps(self.data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.teacher_token}'})
        self.assessment = self.response.get_json().get('assessment')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_make_submission(self):
        response = self.client.post(f'/api/v1/content/assessment/{self.assessment["id"]}/submit',
                                    data=json.dumps(self.answers),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.student_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Assessment submitted successfully.', response.get_data(as_text=True)[:50])
        self.assertIn('message', response.get_data(as_text=True))

    def test_get_assessment_submissions(self):
        response = self.client.post(f'/api/v1/content/assessment/{self.assessment["id"]}/submit',
                                    data=json.dumps(self.answers),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.student_token}'})
        response = self.client.get(f'/api/v1/content/assessment/{self.assessment["id"]}/submissions',
                                    headers={'Authorization': f'Bearer {self.teacher_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('submissions', response.get_data(as_text=True))

    def test_get_user_submission(self):
        response = self.client.post(f'/api/v1/content/assessment/{self.assessment["id"]}/submit',
                                    data=json.dumps(self.answers),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.student_token}'})
        response = self.client.get(f'/api/v1/content/assessment/{self.assessment["id"]}/my-submission',
                                    headers={'Authorization': f'Bearer {self.student_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('submission', response.get_data(as_text=True))

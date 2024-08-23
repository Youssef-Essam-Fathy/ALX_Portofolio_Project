import unittest
from flask import Flask, json
from unittest import TestCase
from app import create_app, db
from app.models.assessment import Assessment
from app.models.user import User, UserRole
from app.models.content import Course, Lesson

class AssessmentAPITestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username='test_user', email='test@example.com', role=UserRole.TEACHER)
        self.test_user.password = 'password'
        db.session.add(self.test_user)
        db.session.commit()

        self.response = self.client.post('/api/v1/auth/login',
                                        data=json.dumps({'username': 'test_user', 'password': 'password'}),
                                        content_type='application/json')
        self.mock_token = json.loads(self.response.get_data(as_text=True))['access_token']

        # Create a test course
        self.test_course = Course(title='Test Course', description='This is a test course.', author=self.test_user)
        db.session.add(self.test_course)
        db.session.commit()

        # Create a test lesson
        self.test_lesson = Lesson(title='Test Lesson', body='This is a test lesson.', course=self.test_course, author=self.test_user)
        db.session.add(self.test_lesson)
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_assessment(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('answers', response.get_data(as_text=True))

    def test_get_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    def test_get_assessment(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    def test_update_assessment(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        data = {'title': 'Updated Sample Assessment'}
        response = self.client.put('/api/v1/content/assessment/1',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    def test_delete_assessment(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.delete('/api/v1/content/assessment/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Assessment deleted successfully', response.get_data(as_text=True))

    # Get all assessments created by a user
    def test_get_user_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/user', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    # Get a specific user assessment by ID
    def test_get_user_assessment(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/user/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    # Get all assessments for a specific lesson
    def test_get_lesson_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/lesson/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    # Get all assessments for a specific course
    def test_get_course_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/course/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    # Get all assessments for a user in a specific course
    def test_get_user_course_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/user/course/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

    # Get all assessments for a user in a specific lesson
    def test_get_user_lesson_assessments(self):

        response = self.client.post('/api/v1/content/assessment',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        response = self.client.get('/api/v1/content/assessment/user/lesson/1', headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Assessment', response.get_data(as_text=True))
        self.assertIn('What is 2+2?', response.get_data(as_text=True))

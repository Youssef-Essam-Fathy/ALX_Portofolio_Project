import unittest
from unittest.mock import patch
from flask import json
from app import create_app, db
from app.models.user import User, UserRole
from app.models.content import Course, Lesson

class TestContentFunctions(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_course(self):
        data = {'title': 'Test Course', 'description': 'This is a test course.'}
        response = self.client.post('/api/v1/content/courses',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Course', response.get_data(as_text=True))

    def test_get_courses(self):
        response = self.client.get('/api/v1/content/courses')
        self.assertEqual(response.status_code, 200)

    def test_get_course(self):
        # First create a course
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/courses/{course.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Course', response.get_data(as_text=True))

    def test_update_course(self):
        # First create a course
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        db.session.commit()

        data = {'title': 'Updated Test Course'}
        response = self.client.put(f'/api/v1/content/courses/{course.id}',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Test Course', response.get_data(as_text=True))

    def test_delete_course(self):
        # First create a course
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        db.session.commit()

        response = self.client.delete(f'/api/v1/content/courses/{course.id}',
                                      headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Course deleted successfully', response.get_data(as_text=True))

    def test_create_lesson(self):
        # First create a course
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        db.session.commit()

        data = {'title': 'Test Lesson', 'body': 'This is a test lesson.', 'course_id': course.id}
        response = self.client.post('/api/v1/content/lessons',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Lesson', response.get_data(as_text=True))

    def test_get_lessons(self):
        response = self.client.get('/api/v1/content/lessons',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)

    def test_update_lesson(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        data = {'title': 'Updated Test Lesson'}
        response = self.client.put(f'/api/v1/content/lessons/{lesson.id}',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Test Lesson', response.get_data(as_text=True))

    def test_delete_lesson(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.delete(f'/api/v1/content/lessons/{lesson.id}',
                                      headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lesson deleted successfully', response.get_data(as_text=True))

    # Get lessons by course
    def test_get_lessons_by_course(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/courses/{course.id}/lessons',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Lesson', response.get_data(as_text=True))

    # Get course by lesson
    def test_get_course_by_lesson(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/lessons/{lesson.id}/course',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Course', response.get_data(as_text=True))

    # Get author by lesson
    def test_get_author_by_lesson(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/lessons/{lesson.id}/author',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_user', response.get_data(as_text=True))

    # Get author by course
    def test_get_author_by_course(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/courses/{course.id}/author',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_user', response.get_data(as_text=True))

    # Get lessons by author
    def test_get_lessons_by_author(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/lessons/by-author/{self.test_user.username}',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Lesson', response.get_data(as_text=True))

    # Get courses by author
    def test_get_courses_by_author(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/courses/by-author/{self.test_user.username}',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Course', response.get_data(as_text=True))

    def test_get_lesson(self):
        # First create a course and a lesson
        course = Course(title='Test Course', description='Test Description', author=self.test_user)
        db.session.add(course)
        lesson = Lesson(title='Test Lesson', body='Test Body', author=self.test_user, course=course)
        db.session.add(lesson)
        db.session.commit()

        response = self.client.get(f'/api/v1/content/lessons/{lesson.id}',
                                   headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Lesson', response.get_data(as_text=True))

    @patch('app.api.v1.content.jwt_required')
    @patch('app.api.v1.content.get_jwt_identity')
    def test_role_required_decorator(self, mock_get_jwt_identity, mock_jwt_required):
        mock_get_jwt_identity.return_value = self.test_user.username

        response = self.client.post('/api/v1/content/courses',
                                    data=json.dumps({'title': 'Test Course', 'description': 'Test'}),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 201)

        # Change user role to student
        self.test_user.role = UserRole.STUDENT
        db.session.commit()

        response = self.client.post('/api/v1/content/courses',
                                    data=json.dumps({'title': 'Test Course 2', 'description': 'Test'}),
                                    content_type='application/json',
                                    headers={'Authorization': f'Bearer {self.mock_token}'})
        self.assertEqual(response.status_code, 403)


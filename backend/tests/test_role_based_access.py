import unittest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models.user import User, UserRole

class RoleBasedAccessTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.admin_user = User(username='admin_user', email='admin@example.com', role=UserRole.ADMIN)
        self.admin_user.password='admin123'
        self.teacher_user = User(username='teacher_user', email='teacher@example.com', role=UserRole.TEACHER)
        self.teacher_user.password='teacher123'
        self.student_user = User(username='student_user', email='student@example.com', role=UserRole.STUDENT)
        self.student_user.password='student123'

        db.session.add_all([self.admin_user, self.teacher_user, self.student_user])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_access(self):
        admin_login = self.client.post('api/v1/auth/login', json={
            'username': 'admin_user',
            'password': 'admin123'
        })
        token = admin_login.get_json().get('access_token')
        response = self.client.get('api/v1/portal/admin', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    def test_teacher_access(self):
        teacher_login = self.client.post('api/v1/auth/login', json={
            'username': 'teacher_user',
            'password': 'teacher123'
        })
        token = teacher_login.get_json().get('access_token')
        response = self.client.get('api/v1/portal/teacher', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    def test_student_access(self):
        student_login = self.client.post('api/v1/auth/login', json={
            'username': 'student_user',
            'password': 'student123'
        })
        token = student_login.get_json().get('access_token')
        response = self.client.get('api/v1/portal/student', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

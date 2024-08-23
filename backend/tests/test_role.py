import unittest
from app import create_app, db
from app.models.user import User, UserRole


class RoleModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_roles(self):
        student = User(username="student", email="student1@email.com", role=UserRole.STUDENT, password="std123")
        teacher = User(username="teacher", email="teacher1@email.com", role=UserRole.TEACHER, password="teacher123")
        admin = User(username="admin", email="admin1@email.com", role=UserRole.ADMIN, password="admin123")

        db.session.add_all([student, teacher, admin])
        db.session.commit()
        
        self.assertEqual(student.role, UserRole.STUDENT)
        self.assertEqual(teacher.role, UserRole.TEACHER)
        self.assertEqual(admin.role, UserRole.ADMIN)

    def test_user_roles_invalid(self):
        response = self.client.post("api/v1/users/", json={
            "username": "student",
            "email": "std1@email.com",
            "passeword": "std123",
            "role": "learner"
        })

        self.assertEqual(response.status_code, 400)

    def test_user_role_not_set(self):
        response = self.client.post("api/v1/users/", json={
            "username": "student",
            "email": "std1@email.com",
            "password": "std123",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['user']['role'], UserRole.STUDENT)
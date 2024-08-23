import unittest
from app import create_app, db
from app.models.user import User, UserRole

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_register(self):
        response = self.client.post('/api/v1/auth/register', json={
            "username": "testregister",
            "email": "testlogin@email.com",
            "password": "mypass145",
            'role': UserRole.STUDENT
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.get_json()['message'])


    def test_login_and_logout(self):
        user = User(username="testlogin", email="testlogin@email.com", password="mypass145")
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/v1/auth/login', json={
            "username": "testlogin",
            "password": "mypass145"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logged in successfully", response.get_json()['message'])

        headers = {
            'Authorization': f'Bearer {response.get_json()["access_token"]}'
        }
        response = self.client.get('/api/v1/auth/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logged out successfully", response.get_json()['message'])

    def test_invalid_login(self):
        user = User(username="testlogin", email="testlogin@email.com", password="mypass145")
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/v1/auth/login', json={
            "username": "fiksja",
            "password": "mypassnot145"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid name or password", response.get_json()['message'])

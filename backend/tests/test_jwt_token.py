import unittest
from flask import json
from app import create_app, db
from app.models.user import User
from flask_jwt_extended import get_jwt_identity, decode_token

class TestJWTValidation(unittest.TestCase):
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

    def test_jwt_when_login(self):
        user = User(username="testlogin", email="testlogin@email.com")
        user.password = "mypass145"
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/api/v1/auth/login', json={
            "username": "testlogin",
            "password": "mypass145"
        })

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))

        # Check if a token was returned
        self.assertIn('access_token', data)
        token = data['access_token']

        # Validate the token
        try:
            decoded_token = decode_token(token)
            self.assertEqual(decoded_token['sub'], "testlogin")
        except jwt.ExpiredSignatureError: # Type: ignore
            self.fail("Token has expired")
        except jwt.InvalidTokenError: # Type: ignore
            self.fail("Token is invalid")

    def test_protected_route_with_valid_token(self):
        # Create a test user
        user = User(username="testprotected", email="testprotected@email.com")
        user.password = "protectedpass145"
        db.session.add(user)
        db.session.commit()

        # Login to get a token
        login_response = self.client.post('/api/v1/auth/login', json={
            "username": "testprotected",
            "password": "protectedpass145"
        })
        token = json.loads(login_response.data.decode('utf-8'))['access_token']

        # Access a protected route
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/api/v1/portal/student', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('Welcome, student!', data['message'])
        self.assertIn('message', data)

    def test_protected_route_with_invalid_token(self):
        # Create an invalid token
        invalid_token = "invalid.token.here"

        # Try to access a protected route with the invalid token
        headers = {'Authorization': f'Bearer {invalid_token}'}
        response = self.client.get('/api/v1/portal/student', headers=headers)

        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Invalid token")

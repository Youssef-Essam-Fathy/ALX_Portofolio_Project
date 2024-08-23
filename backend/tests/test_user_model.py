import unittest
from app import create_app, db
from app.models.user import User, UserRole
from app.models.content import Course, Lesson
from datetime import datetime


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User(
            firstName='John',
            lastName='Doe',
            age=30,
            country='USA',
            email='john@example.com',
            username='johndoe',
            role=UserRole.STUDENT,
            password='password123'
        )
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(email='john@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'johndoe')

    def test_password_verification(self):
        user = User(
            firstName='Jane',
            lastName='Doe',
            age=25,
            country='Canada',
            email='jane@example.com',
            username='janedoe',
            role=UserRole.STUDENT,
            password='password456'
        )
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.verify_password('password456'))
        self.assertFalse(user.verify_password('wrongpassword'))

    def test_update_user(self):
        user = User(
            firstName='Alice',
            lastName='Smith',
            age=28,
            country='UK',
            email='alice@example.com',
            username='alicesmith',
            role=UserRole.STUDENT,
            password='password789'
        )
        db.session.add(user)
        db.session.commit()

        user.firstName = 'Alicia'
        db.session.commit()

        updated_user = User.query.filter_by(email='alice@example.com').first()
        self.assertEqual(updated_user.firstName, 'Alicia')

    def test_delete_user(self):
        user = User(
            firstName='Bob',
            lastName='Brown',
            age=32,
            country='Australia',
            email='bob@example.com',
            username='bobbrown',
            role=UserRole.STUDENT,
            password='password321'
        )
        db.session.add(user)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.filter_by(email='bob@example.com').first()
        self.assertIsNone(deleted_user)
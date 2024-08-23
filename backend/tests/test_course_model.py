import unittest
from app import create_app, db
from app.models.content import Course
from app.models.user import User, UserRole
from datetime import datetime

class CourseModelTestCase(unittest.TestCase):

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

    def test_create_course(self):
        user = User(
            username='admin',
            email='admin@example.com',
            password='admin',
            role=UserRole.ADMIN,
        )
        db.session.add(user)
        db.session.commit()
        course = Course(
            title='Quran Studies',
            description='A comprehensive course on the Quran.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        retrieved_course = Course.query.filter_by(title='Quran Studies').first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.description, 'A comprehensive course on the Quran.')

    def test_update_course(self):
        user = User(
            username='admin',
            email='admin@example.com',
            password='admin',
            role=UserRole.ADMIN,
        )
        db.session.add(user)
        db.session.commit()

        course = Course(
            title='Arabic Studies',
            description='A course on the Arabic language.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        course.title = 'Advanced Arabic Studies'
        db.session.commit()

        updated_course = Course.query.filter_by(description='A course on the Arabic language.').first()
        self.assertEqual(updated_course.title, 'Advanced Arabic Studies')

    def test_delete_course(self):
        user = User(
            username='admin',
            email='admin@example.com',
            password='admin',
            role=UserRole.ADMIN,
        )
        db.session.add(user)
        db.session.commit()
        course = Course(
            title='Islamic Studies',
            description='A course on Islamic teachings.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        db.session.delete(course)
        db.session.commit()

        deleted_course = Course.query.filter_by(title='Islamic Studies').first()
        self.assertIsNone(deleted_course)

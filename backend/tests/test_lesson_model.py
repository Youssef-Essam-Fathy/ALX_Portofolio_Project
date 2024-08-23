import unittest
from app import create_app, db
from app.models.user import User, UserRole
from app.models.content import Lesson, Course
from datetime import datetime

class LessonModelTestCase(unittest.TestCase):

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

    def test_create_lesson(self):
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

        course = Course(
            title='Quran Studies',
            description='A comprehensive course on the Quran.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        lesson = Lesson(
            title='Introduction to Quran',
            body='This is the first lesson.',
            author_id=user.id,
            course_id=course.id
        )
        db.session.add(lesson)
        db.session.commit()

        retrieved_lesson = Lesson.query.filter_by(title='Introduction to Quran').first()
        self.assertIsNotNone(retrieved_lesson)
        self.assertEqual(retrieved_lesson.body, 'This is the first lesson.')

    def test_update_lesson(self):
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

        course = Course(
            title='Arabic Studies',
            description='A course on the Arabic language.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        lesson = Lesson(
            title='Basic Arabic',
            body='This is a lesson on basic Arabic.',
            author_id=user.id,
            course_id=course.id
        )
        db.session.add(lesson)
        db.session.commit()

        lesson.title = 'Advanced Arabic'
        db.session.commit()

        updated_lesson = Lesson.query.filter_by(body='This is a lesson on basic Arabic.').first()
        self.assertEqual(updated_lesson.title, 'Advanced Arabic')

    def test_delete_lesson(self):
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

        course = Course(
            title='Islamic Studies',
            description='A course on Islamic teachings.',
            author=user
        )
        db.session.add(course)
        db.session.commit()

        lesson = Lesson(
            title='Islamic History',
            body='This is a lesson on Islamic history.',
            author_id=user.id,
            course_id=course.id
        )
        db.session.add(lesson)
        db.session.commit()

        db.session.delete(lesson)
        db.session.commit()

        deleted_lesson = Lesson.query.filter_by(title='Islamic History').first()
        self.assertIsNone(deleted_lesson)

import unittest
from app import create_app, db
from app.models.user import User

class TestPasswordHash(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hash(self):
        user = User()
        user.username = "Abdo El-King"
        user.email = "abdoomer1112003@gmail.com"
        user.password = "Abdo123"
        self.assertTrue(user.password_hash is not None)
        with self.assertRaises(AttributeError): # type: ignore
            user.password

    def test_different_salt(self):
        user1 = User()
        user1.username = "Abdo El-King"
        user1.email = "abdoomer1112003@gmail.com"
        user1.password = "Abdo123"
        user2 = User()
        user2.username = "Youssef El-Nemr"
        user2.email = "youssefessam5623@gmail.com"
        user2.password = "Abdo123"

        self.assertTrue(user1.password_hash != user2.password_hash)

    def test_verify_method(self):
        user = User()
        user.username = "Abdo El-King"
        user.email = "abdoomer1112003@gmail.com"
        user.password = "Abdo123"

        self.assertTrue(user.verify_password("Abdo123"))
        self.assertFalse(user.verify_password("Abdo213"))
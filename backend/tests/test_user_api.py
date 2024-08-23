import unittest
from app import create_app, db
from app.models.user import User

class TestUserAPI(unittest.TestCase):
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

    def test_create_user(self):
        response = self.client.post('api/v1/users', json={
            "firstName": "Youssef",
            "lastName": "Essam",
            "age": 22,
            "country": "Egypt",
            "email": "youssefessam5623@gmail.com",
            "username": "Youssef Tiger",
            "password": "123pass"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_json()['message'])

    def test_get_users(self):
        user1 = User()
        user1.email = "abdoomer1112003@gmail.com"
        user1.username = "Abdo El-King"
        user1.password = "Abdo123"

        user2 = User()
        user2.email = "youssefessam5623@gmail.com"
        user2.username = "Youssef El-Nemr"
        user2.password = "Youssef123"
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.get('api/v1/users')


        self.assertEqual(len(response.get_json()), 2) # type: ignore
        self.assertEqual(response.status_code, 200)


    def test_get_user_by_id(self):
        user1 = User()
        user1.email = "abdoomer1112003@gmail.com"
        user1.username = "Abdo El-King"
        user1.password = "Abdo123"

        user2 = User()
        user2.email = "youssefessam5623@gmail.com"
        user2.username = "Youssef El-Nemr"
        user2.password = "Youssef123"
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.get(f'api/v1/users/{user1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['username'], "Abdo El-King")

        response = self.client.get(f'api/v1/users/{user2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['username'], "Youssef El-Nemr")

    def test_update_user(self):
        user1 = User()
        user1.email = "abdoomer1112003@gmail.com"
        user1.username = "Abdo El-King"
        user1.password = "Abdo123"
        user2 = User()
        user2.email = "youssefessam5623@gmail.com"
        user2.username = "Youssef El-Nemr"
        user2.password = "Youssef123"
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.put(f'api/v1/users/{user1.id}', json={
            "email": "new_email1@gmail.com",
            "username": "UniqueUsername1"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User updated successfully', response.get_json()['message'])

        response = self.client.put(f'api/v1/users/{user2.id}', json={
            "email": "new_email2@gmail.com",
            "username": "UniqueUsername2"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User updated successfully', response.get_json()['message'])

    def test_delete_user(self):
        user1 = User()
        user1.email = "abdoomer1112003@gmail.com"
        user1.username = "Abdo El-King"
        user1.password = "Abdo123"
        user2 = User()
        user2.email = "youssefessam5623@gmail.com"
        user2.username = "Youssef El-Nemr"
        user2.password = "Youssef123"
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.delete(f'api/v1/users/{user1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.get_json()['message'])

        response = self.client.delete(f'api/v1/users/{user2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.get_json()['message'])

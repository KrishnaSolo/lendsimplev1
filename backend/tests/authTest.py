import unittest
from unittest.mock import patch
from .. import create_app
from models.user import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass",
        }
        with self.app.app_context():
            db.create_all()

    def test_registration(self):
        response = self.client().post("/auth/register", data=self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Successfully registered", str(response.data))

    def test_login(self):
        response = self.client().post("/auth/register", data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client().post("/auth/login", data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", str(response.data))

    def test_logout(self):
        response = self.client().post("/auth/register", data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client().post("/auth/login", data=login_data)
        self.assertEqual(response.status_code, 200)
        token = response.json["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client().post("/auth/logout", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully logged out", str(response.data))

    def test_token_validity(self):
        response = self.client().post("/auth/register", data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client().post("/auth/login", data=login_data)
        self.assertEqual(response.status_code, 200)
        token = response.json["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client().get("/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test User", str(response.data))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

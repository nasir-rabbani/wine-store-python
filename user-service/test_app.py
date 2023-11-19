import unittest
import app
import json


class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_register_user(self):
        user_data = {
            "username": "testuser",
            "password": "testpass",
            "email": "test@example.com",
        }
        response = self.app.post("/users", json=user_data)
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        response = self.app.get("/user/testuser")
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user_data = {
            "username": "testuser",
            "password": "newpass",
            "email": "newtest@example.com",
        }
        response = self.app.put("/user/testuser", json=user_data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

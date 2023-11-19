import unittest
import app
import json


class OrderServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_create_order(self):
        order_data = {"orderId": "123", "items": ["item1", "item2"], "total": 100}
        response = self.app.post("/orders", json=order_data)
        self.assertEqual(response.status_code, 201)

    def test_get_order(self):
        response = self.app.get("/orders/123")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

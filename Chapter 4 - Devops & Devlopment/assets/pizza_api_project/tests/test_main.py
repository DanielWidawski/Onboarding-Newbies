import unittest

from fastapi.testclient import TestClient

from unittest.mock import patch
from exceptions.exceptions import ValidationError
from main import app
from orders.order_request import OrderRequest
from routers.orders import create_order

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_get_menu(self):
        response = client.get("/menu")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()["menu"]["Pepperoni"]["name"] == "Pepperoni"

    # ==========================================
    # TODO: WRITE TESTS FOR THE POST ENDPOINT
    # ==========================================

    # Example of what is needed:
    @patch('db_handler.database_orm.save_order_to_db', return_value=True)
    def test_create_order_success(self, mock_save_db):
        # 1. Arrange: setup mock return value and payload
        # 2. Act: send POST request to /orders
        # 3. Assert: check status code, response data, and that mock was called
        test_order = {"customer_name": "test", "item_names": ["Margherita"]}
        response = client.post('/orders', json=test_order)
        assert response.status_code == 300
        

    def test_create_order_empty_list(self):
        """TODO: Test that sending an order with no pizzas returns a 400 error."""
        test_order = {"customer_name": "test", "item_names": []}
        with self.assertRaises(ValidationError) as cm:
            create_order(OrderRequest(**test_order))
        self.assertEqual(cm.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()

import unittest

from fastapi.testclient import TestClient

from unittest.mock import patch
from exceptions.exceptions import ValidationError
from main import app
from orders.order_request import OrderRequest
from routers.orders import create_order

client = TestClient(app)


class TestAPI(unittest.TestCase):
    test_order = {"customer_name": "test", "item_names": ["Margherita"]}

    def test_get_menu(self):
        response = client.get("/menu")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()["menu"]["Pepperoni"]["name"] == "Pepperoni"

    # ==========================================
    # TODO: WRITE TESTS FOR THE POST ENDPOINT
    # ==========================================

    @patch("routers.orders.OrderManager.backend_store.save_order")
    def test_create_order_success(self, mock_save_to_db):
        mock_save_to_db.return_value = "12345"
        test_order = {"customer_name": "test", "item_names": ["Margherita"]}
        expected_result = {"order_id": "12345", "total_price": 10.0}
        
        response = client.post("/orders/", json=test_order)
        
        self.assertEqual(response.json(), expected_result)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_save_to_db.called)

    def test_create_order_empty_list(self):
        """TODO: Test that sending an order with no pizzas returns a 400 error."""
        test_order = {"customer_name": "test", "item_names": []}
        with self.assertRaises(ValidationError) as cm:
            create_order(OrderRequest(**test_order))
        self.assertEqual(cm.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()

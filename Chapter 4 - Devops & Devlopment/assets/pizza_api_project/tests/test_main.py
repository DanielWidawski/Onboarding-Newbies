from fastapi.testclient import TestClient

from unittest.mock import patch
from exceptions.exceptions import ValidationError
from main import app
from orders.order_request import OrderRequest
from routers.orders import create_order
import pytest

# Arrange
client = TestClient(app)


class TestAPI:

    def test_get_menu(self):
        # Act
        response = client.get("/menu")
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()["menu"]["Pepperoni"]["name"] == "Pepperoni"

    # Arrange
    @patch("routers.orders.OrderManager.db_handler.save_order")
    def test_create_order_success(self, mock_save_to_db):
        mock_save_to_db.return_value = "12345"
        test_order = {"customer_name": "test", "item_names": ["Margherita"]}
        expected_result = {"order_id": "12345", "total_price": 10.0}

        # Act
        response = client.post("/orders/", json=test_order)

        # Assert
        assert response.json() == expected_result
        assert response.status_code == 200
        assert mock_save_to_db.called

    def test_create_order_empty_list(self):
        # Arrange
        test_order = {"customer_name": "test", "item_names": []}
        # Act + Assert
        with pytest.raises(ValidationError):
            create_order(OrderRequest(**test_order))

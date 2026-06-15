from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from hypothesis import assume, given
from hypothesis import strategies as st

from exceptions.exceptions import ValidationError
from main import app
from models import default_menu
from orders.order_request import OrderRequest
from routers.orders import create_order

# Arrange
client = TestClient(app)


class TestAPI:
    def test_get_menu(self) -> None:
        # Act
        response = client.get("/menu")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()["menu"]["Pepperoni"]["name"] == "Pepperoni"

    # Arrange
    @patch("routers.orders.OrderManager.db_handler.save_order")
    @given(
        item_names=st.lists(
            st.sampled_from(default_menu.get_all_options()),
            max_size=10,
        ),
    )
    def test_create_order_success(
        self,
        mock_save_to_db: MagicMock,
        item_names: list[str],
    ) -> None:

        assume(len(item_names) > 0)

        mock_save_to_db.return_value = "12345"
        test_order = {"customer_name": "test", "item_names": item_names}

        expected_sum = sum(
            [
                default_menu.get_item_by_name(item_name).price
                for item_name in item_names
            ],
        )
        expected_result = {"order_id": "12345", "total_price": expected_sum}

        # Act
        response = client.post("/orders/", json=test_order)

        # Assert
        assert response.json() == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert mock_save_to_db.called

    def test_create_order_empty_list(self) -> None:
        # Arrange
        test_order = {"customer_name": "test", "item_names": []}
        # Act + Assert
        with pytest.raises(ValidationError):
            create_order(OrderRequest(**test_order))

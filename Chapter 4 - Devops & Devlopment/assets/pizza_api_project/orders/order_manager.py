from typing import Any
from uuid import UUID

from db_handler import default_backend
from db_handler.db_handler import DbHandler
from orders.order_request import OrderRequest


class OrderManager:
    db_handler: DbHandler = default_backend

    def manage_order(self, order: OrderRequest) -> dict[str, Any]:
        total = self.calculate_order_total(order)

        return {"order_id": self.save_order(order), "total_price": total}

    def calculate_order_total(self, order: OrderRequest) -> float:
        return sum(item.price for item in order.items)

    def save_order(self, order: OrderRequest) -> UUID:
        return self.db_handler.save_order(order)

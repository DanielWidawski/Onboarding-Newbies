from uuid import UUID

from db_handler.db_handler import DbHandler
from db_handler import default_backend
from models.menu import Menu
from orders.order_request import OrderRequest


class OrderManager:
    db_handler: DbHandler = default_backend

    def manage_order(self, order: OrderRequest, menu: Menu):
        total = self.calculate_order_total(order, menu)

        return {"order_id": self.save_order(order), "total_price": total}

    def calculate_order_total(self, order: OrderRequest, menu: Menu) -> float:
        total = 0
        for item in order.items:
            total += item.price

        return total

    def save_order(self, order: OrderRequest) -> UUID:
        return self.db_handler.save_order(order)

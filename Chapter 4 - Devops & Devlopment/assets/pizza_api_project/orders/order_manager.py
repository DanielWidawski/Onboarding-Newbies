from uuid import UUID

from db_handler.database_orm import save_order_to_db
from models.menu import Menu
from orders.order_request import OrderRequest

    

class OrderManager:
    def manage_order(self, order: OrderRequest, menu: Menu):
        total = self.calculate_order_total(order, menu)
        id = self.save_order(order)
        return {"order_id": id, "total_price": total}
        
    def calculate_order_total(self, order: OrderRequest, menu: Menu) -> float:
        total = 0
        for item in order.items:
            total += item.price
        return total
    
    def save_order(self, order: OrderRequest) -> UUID:
        return save_order_to_db(order)        
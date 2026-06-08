from db_handler.database_orm import save_order_to_db
from models.pizza import OrderRequest
from orders import default_validator_manager
from orders.order_validator import OrderValidatorManager

    

class OrderManager:
    validator: OrderValidatorManager = default_validator_manager
    
    def manage_order(self, order: OrderRequest):
        if self.validator.validate(order) is False:
            raise Exception
        total = self.calculate_order_total(order)
        id = self.save_order(order)
        return {"order_id": id, "total_price": total}
    
        
    def calculate_order_total(self, order: OrderRequest) -> float:
        total = 0
        for pizza in order.pizzas:
            total += pizza.price
        return total
    
    def save_order(self, order: OrderRequest) -> int:
        return save_order_to_db(order.model_dump())        
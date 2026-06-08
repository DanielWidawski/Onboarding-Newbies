from abc import ABC, abstractmethod

from models.pizza import OrderRequest



class OrderValidator(ABC):
    @abstractmethod
    def validate(self, order: OrderRequest) -> bool:
        ...
        
class OrderValidatorManager:
    validators: list[OrderValidator]
    
    def __init__(self, validators: list[OrderValidator]):
        self.validators = validators
    
    def validate(self, order: OrderRequest) -> bool:
        for validator in self.validators:
            if validator.validate(order) is False:
                return False
        return True
    
    
class EmptyOrderValidator(OrderValidator):
    def validate(self, order: OrderRequest) -> bool:
        if order.pizzas:
            return True
        return False
    
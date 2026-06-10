
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return self.name == other.name
    
class PizzaMargherita(Item):
    def __init__(self):
        super().__init__(name="Margherita", price=10.0)
        
class PizzaPepperoni(Item):
    def __init__(self):
        super().__init__(name="Pepperoni", price=12.5)
        
class PizzaVegan(Item):
    def __init__(self):
        super().__init__(name="Vegan", price=11.0)
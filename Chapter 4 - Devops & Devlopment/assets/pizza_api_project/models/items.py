from pizza import PizzaItem

class PizzaMargherita(PizzaItem):
    NAME: str = "Margherita"
    PRICE: float = 10.0
    def __init__(self):
        super().__init__(name=self.NAME, price=self.PRICE)
        
class PizzaPepperoni(PizzaItem):
    NAME: str = "Margherita"
    PRICE: float = 12.5
    def __init__(self):
        super().__init__(name=self.NAME, price=self.PRICE)
        

class PizzaVegan(PizzaItem):
    NAME: str = "Vegan"
    PRICE: float = 11.0
    def __init__(self):
        super().__init__(name=self.NAME, price=self.PRICE)
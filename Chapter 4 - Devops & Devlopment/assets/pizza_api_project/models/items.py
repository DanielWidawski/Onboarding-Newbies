from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class PizzaMargherita(Item):
    def __init__(self) -> None:
        super().__init__(name="Margherita", price=10.0)


class PizzaPepperoni(Item):
    def __init__(self) -> None:
        super().__init__(name="Pepperoni", price=12.5)


class PizzaVegan(Item):
    def __init__(self) -> None:
        super().__init__(name="Vegan", price=11.0)

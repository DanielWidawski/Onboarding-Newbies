from models.items import Item


class Pizza(Item):
    def __init__(self, name: str = "Pizza", price: float = 10.0) -> None:
        super().__init__(name=name, price=price)


class PizzaMargherita(Pizza):
    def __init__(self) -> None:
        super().__init__(name="Margherita", price=10.0)


class PizzaPepperoni(Pizza):
    def __init__(self) -> None:
        super().__init__(name="Pepperoni", price=12.5)


class PizzaVegan(Pizza):
    def __init__(self) -> None:
        super().__init__(name="Vegan", price=11.0)

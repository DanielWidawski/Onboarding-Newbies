from models.menu import Menu
from models.pizza_items import PizzaMargherita, PizzaPepperoni, PizzaVegan

default_menu: Menu = Menu()
default_menu.add_item(PizzaMargherita())
default_menu.add_item(PizzaPepperoni())
default_menu.add_item(PizzaVegan())

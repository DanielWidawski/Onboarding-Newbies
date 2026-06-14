from models.items import PizzaMargherita, PizzaPepperoni, PizzaVegan
from models.menu import DictMenu, Menu

default_menu: Menu = DictMenu()
default_menu.add_item(PizzaMargherita())
default_menu.add_item(PizzaPepperoni())
default_menu.add_item(PizzaVegan())

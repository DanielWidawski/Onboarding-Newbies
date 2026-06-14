from abc import ABC, abstractmethod

from pydantic import BaseModel, InstanceOf

from models.items import Item


class Menu(ABC):
    @abstractmethod
    def add_item(self, item: Item):
        pass

    @abstractmethod
    def remove_item(self, item: Item):
        pass

    @abstractmethod
    def is_item_included(self, item_name: str) -> bool:
        pass

    @abstractmethod
    def get_item_by_name(self, item_name: str) -> Item:
        pass


class DictMenu(Menu, BaseModel):
    menu: dict[str, InstanceOf[Item]] = dict()

    def add_item(self, item: Item):
        if item.name not in self.menu:
            self.menu[item.name] = item

    def remove_item(self, item: Item):
        self.menu.pop(item.name)

    def is_item_included(self, item_name: str) -> bool:
        if item_name in self.menu:
            return True
        
        return False

    def get_item_by_name(self, item_name: str) -> Item:
        return self.menu[item_name]

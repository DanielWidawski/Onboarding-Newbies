from abc import ABC, abstractmethod

from pydantic import BaseModel, InstanceOf

from models.items import Item


class Menu(ABC):
    @abstractmethod
    def add_item(self, item: Item) -> None:
        pass

    @abstractmethod
    def remove_item(self, item: Item) -> None:
        pass

    @abstractmethod
    def is_item_included(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_item_by_name(self, name: str) -> Item:
        pass


class DictMenu(Menu, BaseModel):
    menu: dict[str, InstanceOf[Item]] = dict()

    def add_item(self, item: Item) -> None:
        if item.name not in self.menu:
            self.menu[item.name] = item

    def remove_item(self, item: Item) -> None:
        self.menu.pop(item.name)

    def is_item_included(self, name: str) -> bool:
        if name in self.menu:
            return True

        return False

    def get_item_by_name(self, name: str) -> Item:
        return self.menu[name]

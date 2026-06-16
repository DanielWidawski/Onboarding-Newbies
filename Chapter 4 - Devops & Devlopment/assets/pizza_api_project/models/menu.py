from abc import ABC
from typing import Self

from pydantic import BaseModel, InstanceOf

from models.items import Item


class Menu(ABC, BaseModel):
    menu: dict[str, InstanceOf[Item]] = {}

    def add_item(self: Self, item: Item) -> None:
        if item.name not in self.menu:
            self.menu[item.name] = item

    def remove_item(self: Self, item: Item) -> None:
        self.menu.pop(item.name)

    def is_item_included(self: Self, name: str) -> bool:
        return name in self.menu

    def get_item_by_name(self: Self, name: str) -> Item:
        return self.menu[name]

    def get_all_options(self: Self) -> list[str]:
        return [*self.menu]

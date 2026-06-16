from typing import Self

from pydantic import BaseModel, computed_field, field_validator

from exceptions.exceptions import EmptyListError, ItemNotFoundError
from models import default_menu
from models.items import Item


class OrderRequest(BaseModel):
    customer_name: str
    item_names: list[str]

    @field_validator("item_names", mode="after")
    @classmethod
    def is_empty(cls: type["OrderRequest"], lst: list) -> list:
        if not lst:
            raise EmptyListError(list_name="item_names")

        return lst

    @field_validator("item_names", mode="after")
    @classmethod
    def is_in_menu(cls: type["OrderRequest"], item_names: list[str]) -> list[str]:
        for item_name in item_names:
            if not default_menu.is_item_included(item_name):
                raise ItemNotFoundError(item_name=item_name)

        return item_names

    @computed_field
    @property
    def items(self: Self) -> list[Item]:
        return [
            default_menu.get_item_by_name(item_name)
            for item_name in self.item_names
            if default_menu.is_item_included(item_name)
        ]

from pydantic import BaseModel, Field, computed_field, field_validator


from models import default_menu
from models.items import Item
from exceptions.exceptions import ValidationError


class OrderRequest(BaseModel):
    customer_name: str = Field(frozen=True)
    item_names: list[str]

    @field_validator("item_names", mode="after")
    @classmethod
    def is_empty(cls, lst: list) -> list:
        if not lst:
            raise ValidationError("Order is empty")
        return lst

    @field_validator("item_names", mode="after")
    @classmethod
    def is_in_menu(cls, items: list[str]) -> list[str]:
        for item in items:
            if not default_menu.is_item_included(item):
                raise ValidationError(f"Item {item} does not appear on menu")

        return items

    @computed_field
    @property
    def items(self) -> list[Item]:
        items: list[Item] = list()
        for item_name in self.item_names:
            if default_menu.get_item_by_name(item_name):
                items.append(default_menu.get_item_by_name(item_name))

        return items

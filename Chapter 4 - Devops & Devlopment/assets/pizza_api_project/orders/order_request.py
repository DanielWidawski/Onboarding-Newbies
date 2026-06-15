from pydantic import BaseModel, Field, computed_field, field_validator

from exceptions.exceptions import ValidationError
from models import default_menu
from models.items import Item


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

        return [
            default_menu.get_item_by_name(item_name)
            for item_name in self.item_names
            if default_menu.is_item_included(item_name)
        ]

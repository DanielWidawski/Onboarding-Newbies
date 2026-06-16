from typing import Self

from fastapi import status


class ValidationError(Exception):
    def __init__(
        self: Self,
        message: str,
        status_code: int,
        code: str,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code: str = code


class EmptyListError(ValidationError):
    def __init__(self: Self, list_name: str | None = None) -> None:
        super().__init__(
            message=f"List {list_name} can not be empty",
            status_code=status.HTTP_400_BAD_REQUEST,
            code="EMPTY_LIST_ERROR",
        )


class ItemNotFoundError(ValidationError):
    def __init__(self: Self, item_name: str) -> None:
        super().__init__(
            message=f"item {item_name} not found",
            code="ITEM_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

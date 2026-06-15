from typing import Any

from fastapi import status


class ValidationError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int,
        code: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code: str = code
        self.details = details


class EmptyListError(ValidationError):
    def __init__(self, list_name: str | None = None) -> None:
        super().__init__(
            message=f"List {list_name} can not be empty",
            status_code=status.HTTP_400_BAD_REQUEST,
            code="EMPTY_LIST_ERROR",
            details={"empty_list": list_name} if list_name else {},
        )


class ItemNotFoundError(ValidationError):
    def __init__(self, item_name: str) -> None:
        super().__init__(
            message=f"item {item_name} not found",
            code="ITEM_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": item_name},
        )

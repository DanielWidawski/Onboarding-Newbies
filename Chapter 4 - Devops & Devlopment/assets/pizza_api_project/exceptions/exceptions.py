from typing import Any


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
            status_code=400,
            code="EMPTY_LIST_ERROR",
            details={"empty_list": list_name} if list_name else {},
        )


class NotFoundError(ValidationError):
    def __init__(self, resource: str) -> None:
        super().__init__(
            message=f"{resource} not found",
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details={"resource": resource},
        )

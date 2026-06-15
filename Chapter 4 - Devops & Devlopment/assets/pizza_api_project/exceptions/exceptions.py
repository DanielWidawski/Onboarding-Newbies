from typing import Any


class BaseAppError(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BaseAppError):
    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_FAILED",
            status_code=400,
            details={"field": field} if field else {},
        )

from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """
    Base class for all application exceptions.
    Extend this for specific error types.
    """
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
        

class ValidationError(BaseAppException):
    """App logic validation failed"""
    def __init__(self, message: str, field: str | None = None):
        super().__init__(
            message=message,
            code="VALIDATION_FAILED",
            status_code=400,
            details={"field": field} if field else {}
        )

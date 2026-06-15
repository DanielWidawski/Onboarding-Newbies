from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import ValidationError


async def validation_error_handler(
    request: Request, exc: ValidationError,
    ) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "code": exc.code,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path),
            "details": exc.details,
        },
    )

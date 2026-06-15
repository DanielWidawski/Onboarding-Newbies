from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import BaseAppError


def register_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseAppError)
    async def app_exception_handler(
        request: Request, exc: BaseAppError,
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

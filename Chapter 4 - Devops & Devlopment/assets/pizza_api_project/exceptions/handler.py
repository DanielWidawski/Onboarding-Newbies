from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import BaseAppException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseAppException):
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

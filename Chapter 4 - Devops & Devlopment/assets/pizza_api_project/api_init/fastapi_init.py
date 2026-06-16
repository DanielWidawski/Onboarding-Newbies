from fastapi import FastAPI

from exceptions import exception_handler_mapping
from routers import menu, orders, root


def init_api_app() -> FastAPI:
    app = FastAPI(
        title="Pizza Delivery API",
        exception_handlers=exception_handler_mapping,
    )

    app.include_router(orders.router)
    app.include_router(menu.router)
    app.include_router(root.router)

    return app

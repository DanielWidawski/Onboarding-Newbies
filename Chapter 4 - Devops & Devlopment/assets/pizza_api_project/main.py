import uvicorn
from fastapi import FastAPI

from exceptions.handler import register_exception_handler
from routers import menu, orders

app = FastAPI(title="Pizza Delivery API")

app.include_router(orders.router)
app.include_router(menu.router)

register_exception_handler(app)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the Pizza API"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

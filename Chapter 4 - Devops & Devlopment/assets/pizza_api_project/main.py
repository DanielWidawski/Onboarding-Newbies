from fastapi import FastAPI
import uvicorn
from routers import orders

app = FastAPI(title="Pizza Delivery API")

app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Pizza API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

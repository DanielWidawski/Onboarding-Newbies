import uvicorn

from api_init.fastapi_init import init_api_app

app = init_api_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

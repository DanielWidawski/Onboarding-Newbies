import uvicorn

from api_init import app
from config.settings import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.app.host, port=settings.app.port)

import uvicorn

from api_init.fastapi_init import init_api_app
from settings.api_settings import get_config

app = init_api_app()
config = get_config()

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)

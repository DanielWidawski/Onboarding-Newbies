
from pydantic_settings import BaseSettings

from config.app_config import AppConfig


class Settings(BaseSettings):
    app: AppConfig


settings = Settings(app=AppConfig())

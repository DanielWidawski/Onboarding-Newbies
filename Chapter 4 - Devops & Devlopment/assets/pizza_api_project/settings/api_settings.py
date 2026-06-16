from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    host: str = "0.0.0.0"
    port: int = 8000


@lru_cache
def get_config() -> ApiConfig:
    return ApiConfig()

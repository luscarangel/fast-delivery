from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "development"
    database_url: str

    model_config = SettingsConfigDict(extra="ignore")


@lru_cache
def get_settings():
    return Settings()

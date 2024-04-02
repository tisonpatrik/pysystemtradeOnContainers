from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Utilizes environment variables for secure credential management.
    """

    database_url: PostgresDsn
    test_database_url: PostgresDsn
    max_connections: int = 10
    min_connections: int = 1
    connection_timeout: int = 30

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore

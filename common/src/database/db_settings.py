from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Utilizes environment variables for secure credential management.
    """
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    max_connections: int = 17
    min_connections: int = 2
    connection_timeout: int = 5
    statement_cache_size: int =1000
    max_queries: int=10000
    max_inactive_connection_lifetime: float=60.0

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore

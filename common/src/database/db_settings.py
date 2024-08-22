from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Utilizes environment variables for secure credential management.
    """
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    max_connections: int = 20
    min_connections: int = 1
    connection_timeout: int = 500
    statement_cache_size: int =500
    max_queries: int=50000
    max_inactive_connection_lifetime: float=60.0

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore

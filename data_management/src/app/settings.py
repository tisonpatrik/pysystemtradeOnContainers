from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Utilizes environment variables for secure credential management.
    """

    database_url: Optional[PostgresDsn] = None
    test_database_url: Optional[PostgresDsn] = None

    class Config:
        env_file = ".env"


settings = Settings()

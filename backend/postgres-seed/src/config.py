"""
Module for configuring global settings for the application.
This module uses Pydantic's BaseConfig for parsing and validation of configuration data.
"""

import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
# Load environment variables from a .env file.
load_dotenv()


class GlobalConfig(BaseSettings):
    """
    Class for application-wide configuration settings.
    Reads environment variables and provides default values.
    """
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"

    postgres_user: str = os.getenv("DB_USER")
    postgres_password: str = os.getenv("DB_PASSWORD")
    postgres_server: str = os.getenv("POSTGRES_SERVER")
    postgres_port: int = int(os.getenv("DB_PORT"))
    postgres_db: str = os.getenv("DB_NAME")

    postgres_db_tests: str = os.environ.get("POSTGRES_DB_TESTS", "test_grayfox_db")

    @property
    def database_url(self) -> str:
        """Construct and return the PostgreSQL database URL."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


# Create an instance of the GlobalConfig class.
settings = GlobalConfig()

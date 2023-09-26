"""
Configuration module for the application.

This module defines the configuration class `GlobalConfig` which reads configuration values
from environment variables.
"""

import os

from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class GlobalConfig(BaseConfig):
    """
    Global configuration class.
    This class fetches the values from environment variables using `os.getenv`
    and defines properties to build database connection strings.
    """

    title: str = os.environ.get("TITLE", "Default Title")
    version: str = "1.0.0"
    description: str = os.environ.get("DESCRIPTION", "Default Description")
    openapi_prefix: str = os.environ.get("OPENAPI_PREFIX", "/")
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"
    debug: bool = os.environ.get("DEBUG", "False") == "True"

    postgres_user: str = os.getenv("DB_USER")
    postgres_password: str = os.getenv("DB_PASSWORD")
    postgres_server: str = os.getenv("POSTGRES_SERVER")
    postgres_port: int = int(os.getenv("DB_PORT"))
    postgres_db: str = os.getenv("DB_NAME")

    postgres_db_tests: str = os.environ.get("POSTGRES_DB_TESTS", "test_grayfox_db")
    db_echo_log: bool = debug

    @property
    def database_url(self) -> str:
        """Return the asynchronous database connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )
    @property
    def test_database_url(self) -> str:
        """Return the asynchronous database connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_server}:{self.postgres_port}/{self.postgres_db_tests}"
        )
settings = GlobalConfig()

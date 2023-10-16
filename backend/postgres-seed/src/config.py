"""
Module for configuring global settings for the application.
This module uses Pydantic's BaseConfig for parsing and validation of configuration data.
"""

import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

# Load environment variables from a .env file.


class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Reads environment variables and provides default values.
    """

    title: str = os.environ.get("TITLE", "Слава Україні!")
    version: str = "1.0.2"
    description: str = os.environ.get("DESCRIPTION", "Postgres-seeder")
    openapi_prefix: str = os.environ.get("OPENAPI_PREFIX", "/")
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    api_prefix: str = "/api"

    database_url: PostgresDsn = os.getenv("DB_URL")
    test_database_url: PostgresDsn = os.getenv("TEST_DB_URL")


# Create an instance of the GlobalConfig class.
settings = Settings()

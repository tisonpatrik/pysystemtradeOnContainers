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

    database_url: PostgresDsn = os.getenv("DB_URL")  # type: ignore
    test_database_url: PostgresDsn = os.getenv("TEST_DB_URL")  # type: ignore


# Create an instance of the GlobalConfig class.
settings = Settings()

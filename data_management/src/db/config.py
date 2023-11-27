"""
Module for configuring global settings for the application.
This module uses Pydantic's BaseConfig for parsing and validation of configuration data.
"""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Class for application-wide configuration settings.
    Directly provides configuration values.
    """

    database_url: PostgresDsn = "postgresql+asyncpg://postgres:postgres@postgres/grayfox_db"
    test_database_url: PostgresDsn = "postgresql+asyncpg://postgres:postgres@postgres/test_db"

# Create an instance of the Settings class.
settings = Settings()

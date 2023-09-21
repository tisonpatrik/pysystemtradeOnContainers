"""
Base Config Schema module.

This module provides an abstract base class for defining configuration schemas for data
loading and management in a database. This involves specifying column mappings, SQL commands,
table names, and file paths.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict

logging.basicConfig(level=logging.INFO)


class BaseConfigSchema(ABC):
    """
    Abstract Base Class representing a configuration schema.

    The purpose of this schema is to define standardized structures for configuring
    data loading and management operations, particularly for database interactions.
    """

    @property
    @abstractmethod
    def column_mapping(self) -> Dict[str, str]:
        """
        Abstract method that should return a dictionary mapping
        from source columns to target columns.
        """

    @property
    @abstractmethod
    def sql_command(self) -> str:
        """
        Abstract method that should return the SQL command
        associated with the specific configuration.
        """

    @property
    @abstractmethod
    def table_name(self) -> str:
        """
        Abstract method that should return the table name
        associated with the specific configuration.
        """

    @property
    @abstractmethod
    def origin_csv_file_path(self) -> str:
        """
        Abstract method that should return the original CSV file path
        from which data will be sourced for the specific configuration.
        """

    @property
    def file_path(self) -> str:
        """
        Returns a standardized file path based on the table name.
        """
        return f"/tmp/{self.table_name}.csv"

"""
Spread Cost Schema module.

This module provides a configuration schema specifically for spread cost data.
It defines the necessary column mappings, SQL commands, table names, and file paths
related to spread cost data.
"""

from typing import Dict
from src.db.schemas.base_config_schema import BaseConfigSchema


class SpreadCostSchema(BaseConfigSchema):
    """
    Configuration schema for spread cost data.
    
    This schema is a concrete implementation of the BaseConfigSchema for spread cost data.
    It defines the necessary properties and methods required to interact with the spread cost data.
    """

    @property
    def column_mapping(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping from source columns to target columns for the spread cost data.
        """
        return {"Instrument": "symbol", "SpreadCost": "spread_cost"}

    @property
    def sql_command(self) -> str:
        """
        Returns the SQL command to create the spread_cost table.
        """
        return """
                CREATE TABLE spread_cost (
                    symbol VARCHAR(50) PRIMARY KEY,
                    spread_cost FLOAT
                )
                """

    @property
    def table_name(self) -> str:
        """
        Returns the name of the table associated with the spread cost data.
        """
        return "spread_cost"

    @property
    def origin_csv_file_path(self) -> str:
        """
        Returns the original CSV file path from which the spread cost data will be sourced.
        """
        return "/path/in/container/csvconfig/spreadcosts.csv"

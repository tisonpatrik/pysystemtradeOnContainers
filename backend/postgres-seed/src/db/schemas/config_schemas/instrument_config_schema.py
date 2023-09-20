"""
Instrument Config Schema module.

This module provides a configuration schema specifically for instrument data.
It defines the necessary column mappings, SQL commands, table names, and file paths
related to instrument data.
"""

from typing import Dict
from src.db.schemas.base_config_schema import BaseConfigSchema

class InstrumentConfigSchema(BaseConfigSchema):
    """
    Configuration schema for instrument data.
    
    This schema is a concrete implementation of the BaseConfigSchema for instrument data.
    It defines the necessary properties and methods required to interact with the instrument data.
    """

    @property
    def column_mapping(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping from source columns to target columns
        for the instrument data.
        """
        return {
            "Instrument": "symbol",
            "Description": "description",
            "Pointsize": "pointsize",
            "Currency": "currency",
            "AssetClass": "asset_class",
            "PerBlock": "per_block",
            "Percentage": "percentage",
            "PerTrade": "per_trade",
            "Region": "region",
        }

    @property
    def sql_command(self) -> str:
        """
        Returns the SQL command to create the instrument_config table.
        """
        return """
                CREATE TABLE instrument_config (
                        symbol VARCHAR(50) PRIMARY KEY, 
                        description TEXT, 
                        pointsize FLOAT, 
                        currency VARCHAR(10), 
                        asset_class VARCHAR(50), 
                        per_block FLOAT, 
                        percentage FLOAT, 
                        per_trade INTEGER, 
                        region VARCHAR(50)
                    )
                """

    @property
    def table_name(self) -> str:
        """
        Returns the name of the table associated with the instrument data.
        """
        return "instrument_config"

    @property
    def origin_csv_file_path(self) -> str:
        """
        Returns the original CSV file path from which the instrument data will be sourced.
        """
        return "/path/in/container/csvconfig/instrumentconfig.csv"

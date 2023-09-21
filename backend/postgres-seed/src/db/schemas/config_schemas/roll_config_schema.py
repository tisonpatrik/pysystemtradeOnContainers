"""
Roll Config Schema module.

This module provides a configuration schema specifically for roll data.
It defines the necessary column mappings, SQL commands, table names, and file paths
related to roll data.
"""

from typing import Dict

from src.db.schemas.base_config_schema import BaseConfigSchema


class RollConfigSchema(BaseConfigSchema):
    """
    Configuration schema for roll data.

    This schema is a concrete implementation of the BaseConfigSchema for roll data.
    It defines the necessary properties and methods required to interact with the roll data.
    """

    @property
    def column_mapping(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping from source columns to target columns for the roll data.
        """
        return {
            "Instrument": "symbol",
            "HoldRollCycle": "hold_roll_cycle",
            "RollOffsetDays": "roll_offset_days",
            "CarryOffset": "carry_offset",
            "PricedRollCycle": "priced_roll_cycle",
            "ExpiryOffset": "expiry_offset",
        }

    @property
    def sql_command(self) -> str:
        """
        Returns the SQL command to create the roll_config table.
        """
        return """
                CREATE TABLE roll_config (
                    symbol VARCHAR(50) PRIMARY KEY,
                    hold_roll_cycle VARCHAR(50),
                    roll_offset_days INTEGER,
                    carry_offset INTEGER,
                    priced_roll_cycle VARCHAR(50),
                    expiry_offset INTEGER
                )
                """

    @property
    def table_name(self) -> str:
        """
        Returns the name of the table associated with the roll data.
        """
        return "roll_config"

    @property
    def origin_csv_file_path(self) -> str:
        """
        Returns the original CSV file path from which the roll data will be sourced.
        """
        return "/path/in/container/csvconfig/rollconfig.csv"

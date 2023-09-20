"""
Instrument Metadata Schema module.

This module provides a configuration schema specifically for instrument metadata.
It defines the necessary column mappings, SQL commands, table names, and file paths
related to instrument metadata.
"""

from typing import Dict
from src.db.schemas.base_config_schema import BaseConfigSchema

class InstrumentMetadataSchema(BaseConfigSchema):
    """
    Configuration schema for instrument metadata.
    
    This schema is a concrete implementation of the BaseConfigSchema for instrument metadata.
    It defines the necessary properties and methods required to interact with the metadata related to instruments.
    """

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            "Instrument": "symbol",
            "AssetClass": "asset_class",
            "SubClass": "sub_class",
            "SubSubClass": "sub_sub_class",
            "Style": "style",
            "Country": "country",
            "Duration": "duration",
            "Description": "description",
        }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE instrument_metadata (
                    symbol VARCHAR(50) PRIMARY KEY,
                    asset_class VARCHAR(50),
                    sub_class VARCHAR(50),
                    sub_sub_class VARCHAR(50),
                    description VARCHAR(100)
                )
                """

    @property
    def table_name(self) -> str:
        return "instrument_metadata"

    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/moreinstrumentinfo.csv"

"""
Module for Adjusted Prices Schema.

This module contains the schema for the adjusted_prices table, extending
from BaseConfigSchema to define table-specific column mappings, SQL commands,
and other configurations.

Note: This docstring has been adjusted to provide specific details about the module's
purpose and functionality.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema

class AdjustedPricesSchema(BaseConfigSchema):
    """
    AdjustedPricesSchema Class

    This class defines the schema for the table 'adjusted_prices'. It specifies the
    SQL command for table creation, the table's name, the mapping of column names
    from origin CSV files, and the origin CSV file path for this specific table.

    Attributes:
        column_mapping (Dict[str, str]): A mapping from original CSV column names to DB column names.
        sql_command (str): SQL command for creating the table.
        table_name (str): Name of the table.
        origin_csv_file_path (str): Path to the original CSV file.
    """
    @property
    def column_mapping(self):
        return {"DATETIME": "unix_date_time", "price": "price"}

    @property
    def sql_command(self):
        return """
                CREATE TABLE adjusted_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        return "adjusted_prices"

    @property
    def origin_csv_file_path(self):
        return "/path/in/container/adjusted_prices_csv/"

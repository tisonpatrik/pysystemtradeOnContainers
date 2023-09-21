"""
Module for Multiple Prices Schema.

This module defines the schema for the multiple prices table, which extends
from the BaseConfigSchema. It provides the SQL command for creating the table,
mapping of columns from the original CSV files to the database table, the table name,
and the path where the origin CSV files are located.

Note: This docstring provides specific details about the module's purpose and functionalities.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema

class MultiplePricesSchema(BaseConfigSchema):
    """
    MultiplePricesSchema Class

    This class defines the schema for the 'multiple_prices' table. It includes properties
    to get the SQL command for table creation, the table's name, column mapping from
    the original CSV files, and the path where the origin CSV files can be found.

    Attributes:
        column_mapping (Dict[str, str]): Mapping from original CSV column names to DB column names.
        sql_command (str): SQL command for creating the table.
        table_name (str): Name of the table.
        origin_csv_file_path (str): Path to the original CSV file.
    """
    @property
    def column_mapping(self):
        return {
            "DATETIME": "unix_date_time",
            "CARRY": "carry",
            "CARRY_CONTRACT": "carry_contract",
            "PRICE": "price",
            "PRICE_CONTRACT": "price_contract",
            "FORWARD": "forward",
            "FORWARD_CONTRACT": "forward_contract",
        }
    @property
    def sql_command(self):
        return """
            CREATE TABLE multiple_prices (
                    unix_date_time INTEGER,
                    symbol VARCHAR(50),
                    carry FLOAT, 
                    carry_contract INTEGER, 
                    price FLOAT, 
                    price_contract INTEGER, 
                    forward FLOAT, 
                    forward_contract INTEGER,
                    PRIMARY KEY (unix_date_time, symbol)
                )
            """
    @property
    def table_name(self):
        return "multiple_prices"

    @property
    def origin_csv_file_path(self):
        return "/path/in/container/multiple_prices_csv/"

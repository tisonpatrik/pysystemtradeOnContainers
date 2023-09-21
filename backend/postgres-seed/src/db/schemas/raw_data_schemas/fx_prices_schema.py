"""
Module for FX Prices Schema.

This module defines the schema for the foreign exchange prices table, which is an extension
of the BaseConfigSchema. It provides the SQL command for table creation, column mapping
from the original CSV to the database, table name, and the path of the origin CSV file.

Note: This docstring elaborates on the module's purpose and functionalities.
"""
from src.db.schemas.base_config_schema import BaseConfigSchema

class FxPricesSchema(BaseConfigSchema):
    """
    FxPricesSchema Class

    This class defines the schema for the 'fx_prices' table. It provides properties
    to get the SQL command for table creation, the table's name, the column mapping from
    the original CSV files, and the path where the origin CSV files are stored.

    Attributes:
        column_mapping (Dict[str, str]): A mapping from original CSV column names to DB column names.
        sql_command (str): SQL command for creating the table.
        table_name (str): Name of the table.
        origin_csv_file_path (str): Path to the original CSV file.
    """
    @property
    def column_mapping(self):
        return {"DATETIME": "unix_date_time", "PRICE": "price"}

    @property
    def sql_command(self):
        return """
                CREATE TABLE fx_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        return "fx_prices"

    @property
    def origin_csv_file_path(self):
        return "/path/in/container/fx_prices_csv/"

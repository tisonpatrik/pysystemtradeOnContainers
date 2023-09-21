"""
Module for Roll Calendars Schema.

This module defines the schema for the roll calendars table, extending from the BaseConfigSchema. 
It provides the SQL command for creating the table, a mapping of columns from the original CSV 
files to the database table, the table name, and the path where the origin CSV files are located.

Note: This docstring provides specific details about the module's purpose and functionalities.
"""

from src.db.schemas.base_config_schema import BaseConfigSchema

class RollCalendarsSchema(BaseConfigSchema):
    """
    RollCalendarsSchema Class

    This class defines the schema for the 'roll_calendars' table. It includes properties
    to obtain the SQL command for table creation, the table's name, and a mapping of columns 
    from the original CSV files to the database table, as well as the path where the origin 
    CSV files can be found.

    Attributes:
        column_mapping (Dict[str, str]): Mapping from original CSV column names to DB column names.
        sql_command (str): SQL command for creating the table.
        table_name (str): Name of the table.
        origin_csv_file_path (str): Path to the original CSV file.
    """
    @property
    def column_mapping(self):
        return {
            "DATE_TIME": "unix_date_time",
            "current_contract": "current_contract",
            "next_contract": "next_contract",
            "carry_contract": "carry_contract",
        }

    @property
    def sql_command(self):
        return """
                CREATE TABLE roll_calendars (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        current_contract INTEGER,
                        next_contract INTEGER,
                        carry_contract INTEGER,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """

    @property
    def table_name(self):
        return "roll_calendars"

    @property
    def origin_csv_file_path(self):
        return "/path/in/container/roll_calendars_csv/"

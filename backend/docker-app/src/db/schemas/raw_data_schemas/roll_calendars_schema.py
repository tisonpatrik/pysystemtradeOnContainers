from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class RollCalendarsSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'DateTime': 'unix_date_time',
            'Instrument': 'symbol',
            'CurrentContract': 'current_contract',
            'NextContract': 'next_contract',
            'CarryContract': 'carry_contract'
        }

    @property
    def sql_command(self) -> str:
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
    def table_name(self) -> str:
        return "roll_calendars"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/roll_calendars_csv/"

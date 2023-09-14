from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class RollConfigSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
                'Instrument': 'symbol',
                'HoldRollCycle': 'hold_roll_cycle',
                'RollOffsetDays': 'roll_offset_days',
                'CarryOffset': 'carry_offset',
                'PricedRollCycle': 'priced_roll_cycle',
                'ExpiryOffset': 'expiry_offset'
                }


    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE roll_config (
                    SYMBOL VARCHAR(255) PRIMARY KEY,
                    HOLD_ROLL_CYCLE VARCHAR(255),
                    ROLL_OFFSET_DAYS INTEGER,
                    CARRY_OFFSET INTEGER,
                    PRICED_ROLL_CYCLE VARCHAR(255),
                    EXPIRY_OFFSET INTEGER
                )
                """
    
    @property
    def table_name(self) -> str:
        return "roll_config"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/rollconfig.csv"
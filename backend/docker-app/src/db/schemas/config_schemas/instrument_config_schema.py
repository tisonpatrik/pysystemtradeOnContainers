from src.db.schemas.config_schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class InstrumentConfigSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'Instrument': 'symbol', 
            'Description': 'description', 
            'Pointsize': 'pointsize', 
            'Currency': 'currency', 
            'AssetClass': 'asset_class', 
            'PerBlock': 'per_block', 
            'Percentage': 'percentage', 
            'PerTrade': 'per_trade', 
            'Region': 'region'
            }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE instrument_config (
                        SYMBOL VARCHAR(255) PRIMARY KEY, 
                        DESCRIPTION TEXT, 
                        POINTSIZE FLOAT, 
                        CURRENCY VARCHAR(10), 
                        ASSET_CLASS VARCHAR(50), 
                        PER_BLOCK FLOAT, 
                        PERCENTAGE FLOAT, 
                        PER_TRADE INTEGER, 
                        REGION VARCHAR(50)
                    )
                """
    
    @property
    def table_name(self) -> str:
        return "instrument_config"
    
    @property
    def csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/instrumentconfig.csv"
from src.db.schemas.config_schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class SpreadCostSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
                'Instrument': 'symbol', 
                'SpreadCost': 'spread_cost'
                }


    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE spread_cost (
                    SYMBOL VARCHAR(255) PRIMARY KEY,
                    SPREAD_COST FLOAT
                )
                """
    
    @property
    def table_name(self) -> str:
        return "spread_cost"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/csvconfig/spreadcosts.csv"
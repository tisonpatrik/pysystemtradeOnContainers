from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class FxPricesSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'DateTime': 'unix_date_time',
            'Instrument': 'symbol',
            'Price': 'price'
        }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE fx_prices (
                        unix_date_time INTEGER PRIMARY KEY,
                        symbol VARCHAR(50) PRIMARY KEY,
                        price FLOAT
                    )
                """
    
    @property
    def table_name(self) -> str:
        return "fx_prices"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/fx_prices_csv/"
from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class AdjustedPricesSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'DateTime': 'unix_date_time',
            'Instrument': 'symbol',
            'Adjusted_Price': 'price'
        }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE adjusted_prices (
                        unix_date_time INTEGER,
                        symbol VARCHAR(50),
                        adjusted_price FLOAT,
                        PRIMARY KEY (unix_date_time, symbol)
                    )
                """
    
    @property
    def table_name(self) -> str:
        return "adjusted_prices"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/adjusted_prices_csv/"
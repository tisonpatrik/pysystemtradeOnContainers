from src.db.schemas.base_config_schema import BaseConfigSchema
from typing import Dict

class MultiplePricesSchema(BaseConfigSchema):

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            'DateTime': 'date_time',
            'Instrument': 'symbol', 
            'Carry': 'carry', 
            'CarryContract': 'carry_contract', 
            'Price': 'price', 
            'PriceContract': 'price_contract',
            'Forward': 'forward',
            'ForwardContract': 'forward_contract'
            }

    @property
    def sql_command(self) -> str:
        return """
                CREATE TABLE instrument_config (
                        date_time INTEGER PRIMARY KEY,
                        symbol VARCHAR(50) PRIMARY KEY,
                        carry FLOAT, 
                        carry_contract INTEGER, 
                        price FLOAT, 
                        price_contract INTEGER, 
                        forward FLOAT, 
                        forward_contract INTEGER
                    )
                """
    
    @property
    def table_name(self) -> str:
        return "multiple_prices"
    
    @property
    def origin_csv_file_path(self) -> str:
        return "/path/in/container/multiple_prices_csv/"
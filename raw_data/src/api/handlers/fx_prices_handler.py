from common.src.database.repository import Repository
from common.src.database.statement import Statement
from raw_data.src.models.instrument_config_models import Instrument


class FxPricesHandler:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def get_fx_prices_for_symbol_async(self, symbol: Instrument):
        query = "SELECT currency FROM instrument_config WHERE symbol = $1"
        statement = Statement(table_name="fx_prices", query=query, parameters=symbol.symbol)
        instrument_currency = await self.repository.fetch_item_async(statement)
        return instrument_currency

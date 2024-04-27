from common.src.database.repository import Repository
from common.src.database.statements.fetch_statement import FetchStatement


class FxPricesHandler:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def get_fx_prices_for_symbol_async(self, symbol):
        query = "SELECT currency FROM instrument_config WHERE symbol = $1"
        statement = FetchStatement(query=query, parameters=symbol)
        instrument_currency = await self.repository.fetch_item_async(statement)
        return instrument_currency

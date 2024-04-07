from common.src.database.repository import Repository
from common.src.database.statement import Statement
from raw_data.src.models.instrument_config_models import Instrument, InstrumentConfigModel
from raw_data.src.models.raw_data_models import FxPricesModel


class FxPricesHandler:
    def __init__(
        self,
        fx_prices_repository: Repository[FxPricesModel],
        instrument_config_repository: Repository[InstrumentConfigModel],
    ):
        self.fx_prices_repository = fx_prices_repository
        self.instrument_config_repository = instrument_config_repository

    async def get_fx_prices_for_symbol_async(self, symbol: Instrument):
        query = "SELECT currency FROM instrument_config WHERE symbol = $1"
        statement = Statement(query=query, parameters=symbol.symbol)
        instrument_currency = await self.instrument_config_repository.fetch_item_async(statement)
        print(instrument_currency)

        # fx_prices = await self.fx_prices_repository.fetch_many_async(statement)

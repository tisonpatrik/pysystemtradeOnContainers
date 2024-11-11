import pandas as pd

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.repositories.prices_client import PricesClient
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(
        self,
        prices_repository: PricesClient,
        instruments_repository: InstrumentsClient,
        daily_returns_vol_handler: DailyReturnsVolHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_handler = daily_returns_vol_handler
        self.prices_repository = prices_repository
        self.instruments_repository = instruments_repository
        self.instrument_vol_service = InstrumentCurrencyVolService()

    async def get_instrument_vol_for_symbol_async(self, query: GetInstrumentCurrencyVolQuery) -> pd.Series:
        self.logger.info("Fetching instrument currency volatility for %s.", query.symbol)
        denom_prices = await self.prices_repository.get_denom_prices_async(query.symbol)
        point_size = await self.instruments_repository.get_point_size_async(query.symbol)

        daily_returns_vol = await self.daily_returns_vol_handler.get_daily_returns_vol_async(query.symbol)
        return self.instrument_vol_service.calculate_instrument_vol_async(denom_prices, daily_returns_vol, point_size.pointsize)

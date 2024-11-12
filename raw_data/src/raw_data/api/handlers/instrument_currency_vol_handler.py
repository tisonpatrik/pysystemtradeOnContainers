import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.repositories.prices_client import PricesClient
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(
        self,
        prices_repository: PricesClient,
        instruments_repository: InstrumentsClient,
        daily_percentage_volatility_handler: DailyPercentageVolatilityHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_volatility_handler = daily_percentage_volatility_handler
        self.prices_repository = prices_repository
        self.instruments_repository = instruments_repository
        self.instrument_vol_service = InstrumentCurrencyVolService()

    async def get_instrument_vol_for_symbol_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching instrument currency volatility for %s.", symbol)
        denom_prices = await self.prices_repository.get_denom_prices_async(symbol)
        point_size = await self.instruments_repository.get_point_size_async(symbol)
        daily_returns_vol = await self.daily_percentage_volatility_handler.get_daily_percentage_volatility_async(symbol)
        return self.instrument_vol_service.calculate_instrument_vol(denom_prices, daily_returns_vol, point_size.pointsize)

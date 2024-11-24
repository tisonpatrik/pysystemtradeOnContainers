import pandas as pd

from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.prices_client import PricesClient
from common.src.logging.logger import AppLogger
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class InstrumentCurrencyVolHandler:
    def __init__(
        self,
        prices_client: PricesClient,
        instruments_client: InstrumentsClient,
        daily_percentage_volatility_handler: DailyPercentageVolatilityHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_volatility_handler = daily_percentage_volatility_handler
        self.prices_client = prices_client
        self.instruments_client = instruments_client
        self.instrument_vol_service = InstrumentCurrencyVolService()

    async def get_instrument_vol_for_symbol_async(self, symbol: str) -> pd.Series:
        self.logger.info("Fetching instrument currency volatility for %s.", symbol)
        denom_prices = await self.prices_client.get_denom_prices_async(symbol)
        point_size = await self.instruments_client.get_point_size_async(symbol)
        daily_returns_vol = await self.daily_percentage_volatility_handler.get_daily_percentage_volatility_async(symbol)
        return self.instrument_vol_service.calculate_instrument_vol(denom_prices, daily_returns_vol, point_size)

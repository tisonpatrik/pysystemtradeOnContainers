import pandas as pd

from common.src.clients.prices_client import PricesClient
from common.src.logging.logger import AppLogger
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler


class DailyPercentageReturnsHandler:
    def __init__(
        self,
        prices_client: PricesClient,
        daily_returns_handler: DailyReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_client = prices_client
        self.daily_returns_handler = daily_returns_handler

    async def get_daily_percentage_returns_async(self, symbol: str) -> pd.Series:
        denom_prices = await self.prices_client.get_denom_prices_async(symbol)
        num_returns = await self.daily_returns_handler.get_daily_returns_async(symbol)
        return num_returns / denom_prices.ffill()

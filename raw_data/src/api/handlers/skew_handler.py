import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.src.services.skew_service import SkewService


class SkewHandler:
    def __init__(self, daily_percentage_returns_handler: DailyPercentageReturnsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_returns_handler = daily_percentage_returns_handler
        self.skew_service = SkewService()

    async def get_skew_async(self, symbol: str, lookback: int) -> pd.Series:
        try:
            perc_returns = await self.daily_percentage_returns_handler.get_daily_percentage_returns_async(symbol)
            return await self.skew_service.calculate_skew(perc_returns, lookback)
        except Exception:
            self.logger.exception("Error in fetching skew")
            raise

    async def get_neg_skew_async(self, symbol: str, lookback: int) -> pd.Series:
        try:
            perc_returns = await self.daily_percentage_returns_handler.get_daily_percentage_returns_async(symbol)
            return await self.skew_service.calculate_neg_skew(perc_returns, lookback)
        except Exception:
            self.logger.exception("Error in fetching negative skew")
            raise

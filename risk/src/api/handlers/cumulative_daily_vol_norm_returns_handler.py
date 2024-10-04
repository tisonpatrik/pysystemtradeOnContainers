import pandas as pd

from common.src.logging.logger import AppLogger
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class CumulativeDailyVolNormReturnsHandler:
    def __init__(self, daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler

    async def get_cumulative_daily_vol_normalized_returns_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Fetching cumulative daily vol normalized returns for asset class %s", symbol)
            norm_returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns_async(symbol)
            return norm_returns.cumsum()
        except Exception:
            self.logger.exception("Unexpected error occurred while fetching normalied prices for asset class")
            raise

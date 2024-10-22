import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.src.validation.factor_name import FactorName


class SkewHandler:
    def __init__(self, daily_percentage_returns_handler: DailyPercentageReturnsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_percentage_returns_handler = daily_percentage_returns_handler

    async def get_skew_async(self, symbol: str, factor_name: FactorName, lookback: int) -> pd.Series:
        try:
            perc_returns = await self.daily_percentage_returns_handler.get_daily_percentage_returns_async(symbol)
            return perc_returns.rolling(lookback).skew()
        except Exception:
            self.logger.exception("Error in fetching skew")
            raise

    async def get_neg_skew_async(self, symbol: str, factor_name: FactorName, lookback: int) -> pd.Series:
        try:
            return -await self.get_skew_async(symbol, factor_name, lookback)
        except Exception:
            self.logger.exception("Error in fetching negative skew")
            raise

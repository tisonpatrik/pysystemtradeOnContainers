import pandas as pd

from common.src.logging.logger import AppLogger


class SkewService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    async def calculate_skew(self, perc_returns: pd.Series, lookback: int) -> pd.Series:
        """Calculate the skew of the percentage returns."""
        try:
            return perc_returns.rolling(lookback).skew()
        except Exception:
            self.logger.exception("Error in calculating skew")
            raise

    async def calculate_neg_skew(self, perc_returns: pd.Series, lookback: int) -> pd.Series:
        """Calculate the negative skew of the percentage returns."""
        try:
            return -await self.calculate_skew(perc_returns, lookback)
        except Exception:
            self.logger.exception("Error in calculating negative skew")
            raise

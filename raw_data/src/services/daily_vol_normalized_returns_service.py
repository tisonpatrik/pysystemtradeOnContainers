import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.volatility import daily_returns


class DailyVolnormalizedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_daily_vol_normalized_returns(self, prices: pd.Series, returnvol_data: pd.Series) -> pd.Series:
        try:
            returnvol = returnvol_data.shift(1)
            dailyreturns = daily_returns(prices)
            return dailyreturns / returnvol
        except Exception:
            self.logger.exception("Unexpected error occurred while calculating Daily volatility normalized returns")
            raise

import pandas as pd

from common.src.logging.logger import AppLogger


class DailyVolnormalizedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_daily_vol_normalized_returns(self, prices: pd.Series, returnvol_data: pd.Series, dailyreturns: pd.Series) -> pd.Series:
        try:
            returnvol = returnvol_data.shift(1)
            return dailyreturns / returnvol
        except Exception:
            self.logger.exception("Unexpected error occurred while calculating Daily volatility normalized returns")
            raise

import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.volatility import daily_returns


class DailyVolNormalisedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_daily_vol_normalised_returns(self, prices: pd.Series, returnvol_data: pd.Series) -> pd.Series:
        try:
            returnvol = returnvol_data.shift(1)
            dailyreturns = daily_returns(prices)
            norm_return = dailyreturns / returnvol
            return norm_return
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while calculating Daily volatility normalised returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

import pandas as pd

from common.src.logging.logger import AppLogger


class CumulativeDailyVolNormalizedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_cumulative_daily_vol_normalized_returns(self, norm_returns: pd.Series) -> pd.Series:
        try:
            return norm_returns.cumsum()
        except Exception:
            self.logger.exception("Unexpected error occurred while calculating Cumulative Daily volatility normalized returns")
            raise

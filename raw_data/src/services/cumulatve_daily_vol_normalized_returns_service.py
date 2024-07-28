import pandas as pd

from common.src.logging.logger import AppLogger


class CumulativeDailyVolNormalizedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_cumulative_daily_vol_normalised_returns(self, norm_returns: pd.Series) -> pd.Series:
        try:
            cum_norm_returns = norm_returns.cumsum()
            return cum_norm_returns
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while calculating Cumulative Daily volatility normalised returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

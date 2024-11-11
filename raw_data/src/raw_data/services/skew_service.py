import pandas as pd

from common.src.logging.logger import AppLogger


class SkewService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_skew(self, perc_returns: pd.Series, lookback_days: int) -> pd.Series:
        """Calculate the skew of the percentage returns."""
        try:
            lookback_period = pd.Timedelta(days=lookback_days)
            return perc_returns.rolling(lookback_period).skew()
        except Exception:
            self.logger.exception("Error in calculating skew")
            raise

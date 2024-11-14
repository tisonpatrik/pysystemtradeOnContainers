import pandas as pd

from common.src.logging.logger import AppLogger


class MomentumService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_ewmac(self, price: pd.Series, vol: pd.Series, lfast: int, lslow: int):
        try:
            fast_ewma = price.ewm(span=lfast, min_periods=1).mean()
            slow_ewma = price.ewm(span=lslow, min_periods=1).mean()
            raw_ewmac = fast_ewma - slow_ewma

            return raw_ewmac / vol.ffill()
        except Exception as e:
            self.logger.exception("Error occurred in EWMAC calculation")
            raise ValueError("Failed to compute EWMAC due to invalid inputs or unexpected data issues.") from e

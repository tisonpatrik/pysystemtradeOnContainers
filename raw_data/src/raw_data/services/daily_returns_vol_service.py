import pandas as pd

from common.logging.logger import AppLogger
from common.utils.volatility import mixed_vol_calc


class DailyReturnsVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_daily_returns_vol(self, prices, price_returns) -> pd.Series:
        try:
            vol_multiplier = 1
            raw_vol = mixed_vol_calc(price_returns)

            return vol_multiplier * raw_vol

        except Exception:
            self.logger.exception("Unexpected error occurred while calculating daily returns volatility")
            raise

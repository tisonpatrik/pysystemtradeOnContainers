import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.volatility import daily_returns, mixed_vol_calc


class DailyReturnsVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_daily_returns_vol(self, prices) -> pd.Series:
        try:
            price_returns = daily_returns(prices)
            vol_multiplier = 1
            raw_vol = mixed_vol_calc(price_returns)

            return vol_multiplier * raw_vol

        except Exception:
            self.logger.exception("Unexpected error occurred while calculating daily returns volatility")
            raise

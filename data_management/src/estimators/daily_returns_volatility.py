import pandas as pd
from src.estimators.volatility import mixed_vol_calc

from common.logging.logging import AppLogger


class DailyReturnsVolEstimator:
    """
    Class for calculating daily returns volatility of financial instruments.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def process_daily_returns_vol(self, daily_prices: pd.Series) -> pd.Series:
        """
        Process and calculate the volatility for a given instrument configuration.
        """
        try:
            price_returns = self.daily_returns(daily_prices)
            vol_multiplier = 1
            raw_vol = mixed_vol_calc(price_returns)

            vol = vol_multiplier * raw_vol
            return vol

        except Exception as exc:
            error_message = f"General error processing daily returns volatility: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def daily_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Gets daily returns (not % returns)
        """
        dailyreturns = daily_prices.diff()
        return dailyreturns

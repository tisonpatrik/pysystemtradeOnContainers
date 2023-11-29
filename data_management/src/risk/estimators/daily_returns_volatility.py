import pandas as pd
from src.core.utils.logging import AppLogger
from src.risk.errors.daily_returns_vol_processing_error import (
    DailyReturnsVolProcessingHaltedError,
)
from src.risk.estimators.volatility import mixed_vol_calc


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
            # Calculate daily returns
            price_returns = self.daily_returns(daily_prices)
            # vol_multiplier can be adjusted as per your requirement
            vol_multiplier = 1
            raw_vol = mixed_vol_calc(price_returns)

            # Apply the multiplier to the volatility
            # Assuming 'volatility' is the column name in the raw_vol DataFrame
            vol = vol_multiplier * raw_vol
            return vol

        except Exception as exc:
            self.logger.error(
                f"General error processing daily returns volatility: {exc}"
            )
            raise DailyReturnsVolProcessingHaltedError()

    def daily_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Gets daily returns (not % returns)
        """
        dailyreturns = daily_prices.diff()
        return dailyreturns

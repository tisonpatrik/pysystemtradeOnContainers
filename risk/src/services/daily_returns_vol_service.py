"""Module for calculating robust volatility for financial instruments."""

import pandas as pd
from pandera.typing import Series

from common.src.logging.logger import AppLogger
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from risk.src.estimators.volatility import mixed_vol_calc
from risk.src.schemas.risk_schemas import Volatility


class DailyReturnsVolService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.estimator = DailyReturnsVolEstimator()

    def calculate_daily_returns_vol(self, prices) -> Series[Volatility]:
        """
        Calculates and inserts daily returns volatility for given prices.
        """
        try:
            price_returns = self.daily_returns(prices)
            vol_multiplier = 1
            raw_vol = mixed_vol_calc(price_returns)

            vol = vol_multiplier * raw_vol
            return Series[Volatility](vol)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def daily_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Gets daily returns (not % returns)
        """
        dailyreturns = daily_prices.diff()
        return dailyreturns

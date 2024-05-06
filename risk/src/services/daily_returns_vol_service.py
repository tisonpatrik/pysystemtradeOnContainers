"""Module for calculating robust volatility for financial instruments."""

from pandera.typing import Series

from common.src.logging.logger import AppLogger
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
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
            daily_returns_vols = self.estimator.process_daily_returns_vol(prices)
            return Series[Volatility](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

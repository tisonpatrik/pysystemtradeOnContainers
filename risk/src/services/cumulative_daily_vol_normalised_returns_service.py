from pandera.typing import Series

from common.src.logging.logger import AppLogger
from risk.src.estimators.comulative_vol_normalised_returns import CumulativeVolNormalisedReturns
from risk.src.schemas.risk_schemas import DailyVolNormalizedReturnsSchema, Volatility


class CumulativeDailyVolatilityNormalisedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.estimator = CumulativeVolNormalisedReturns()

    def calculate_cumulative_vol_for_prices(self, normalised_returns: Series[DailyVolNormalizedReturnsSchema]):
        """
        Calculate cumulative returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            cumulative_normalised_returns = self.estimator.get_cumulative_daily_vol_normalised_returns(
                normalised_returns
            )
            return Series[Volatility](cumulative_normalised_returns)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

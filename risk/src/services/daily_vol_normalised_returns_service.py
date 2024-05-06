from pandera.typing import Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from risk.src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns
from risk.src.schemas.risk_schemas import Volatility


class DailyVolatilityNormalisedReturnsService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyVolNormalisedReturns()

    def calculate_daily_vol_normalised_returns(self, daily_prices) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_daily_vol_normalised_returns(daily_prices)
            cleaned = daily_returns_vols.dropna()
            return Series[Volatility](cleaned)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

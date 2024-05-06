import pandas as pd
from pandera.typing import Series

from common.src.logging.logger import AppLogger
from risk.src.estimators.instrument_currency_volatility import InstrumentCurrencyVolEstimator
from risk.src.schemas.risk_schemas import Volatility


class InstrumentCurrencyVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.estimator = InstrumentCurrencyVolEstimator()

    def calculate_instrument_vol_async(
        self, denom_price: pd.Series, daily_returns_vol: pd.Series, point_size: float
    ) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_instrument_currency_vol(denom_price, daily_returns_vol, point_size)
            return Series[Volatility](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

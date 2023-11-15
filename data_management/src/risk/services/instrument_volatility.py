
import pandas as pd

from src.risk.estimators.instrument_volatility import get_instrument_currency_vol
from src.common_utils.utils.data_to_db.series_to_frame import process_series_to_frame

from src.risk.models.risk_models import InstrumentVolatility
from src.utils.logging import AppLogger

INSTRUMENT_VOLATILITY_COLUMN_MAPPING = {"price": "volatility"}

class InstrumentVolatilityService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_instrument_volatility_for_instrument(
        self,
        multiple_prices: pd.Series,
        daily_prices: pd.Series,
        poinsize: float,
        symbol: str,
    ) -> pd.DataFrame:
        try:
            volatility = get_instrument_currency_vol(multiple_prices, daily_prices, poinsize)
            data_frame = process_series_to_frame(volatility,symbol,InstrumentVolatility,INSTRUMENT_VOLATILITY_COLUMN_MAPPING)
            return data_frame
        except Exception as error:
            self.logger.error("Failed to calculate volatility for instrument %s: %s",error, exc_info=True)
            raise

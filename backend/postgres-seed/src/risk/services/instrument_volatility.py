import logging

import pandas as pd

# pylint: disable=import-error
from shared.src.estimators.instrument_volatility import get_instrument_currency_vol
from src.common_utils.utils.data_to_db.series_to_frame import (
    process_series_to_frame,
)

from src.core.models.risk_schemas import InstrumentVolatility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTRUMENT_VOLATILITY_COLUMN_MAPPING = {"price": "volatility"}


class InstrumentVolatilityService:
    
    def calculate_instrument_volatility_for_instrument(
        self,
        multiple_prices: pd.Series,
        adjusted_prices: pd.Series,
        symbol: str,
        poinsize: float,
    ) -> pd.DataFrame:
        try:
            volatility = get_instrument_currency_vol(
                multiple_prices, adjusted_prices, poinsize
            ).dropna()
            data_frame = process_series_to_frame(
                volatility,
                symbol,
                InstrumentVolatility,
                INSTRUMENT_VOLATILITY_COLUMN_MAPPING,
            )
            return data_frame
        except Exception as error:
            logger.error(
                "Failed to calculate volatility for instrument %s: %s",
                symbol,
                error,
                exc_info=True,
            )
            raise

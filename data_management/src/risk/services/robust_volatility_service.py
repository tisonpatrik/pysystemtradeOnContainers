"""Module for calculating robust volatility for financial instruments."""

import logging

import pandas as pd

# pylint: disable=import-error
from src.risk.estimators.volatility import robust_vol_calc
from src.common_utils.utils.data_to_db.series_to_frame import (
    process_series_to_frame,
)

from src.core.models.risk_schemas import RobustVolatility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROBUST_VOLATILITY_COLUMN_MAPPING = {"price": "volatility"}


class RobustVolatilityService:
    """
    Service for calculating robust volatility of financial instruments.
    """

    def calculate_robust_volatility_for_instrument(
        self, series: pd.Series, symbol: str
    ) -> pd.DataFrame:
        """
        Calculates the volatility of a given financial instrument represented by a Pandas Series.
        """
        try:
            volatility = robust_vol_calc(series).dropna()
            data_frame = process_series_to_frame(
                volatility, symbol, RobustVolatility, ROBUST_VOLATILITY_COLUMN_MAPPING
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

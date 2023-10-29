"""Module for calculating robust volatility for financial instruments."""

import logging

import pandas as pd

# pylint: disable=import-error
from shared.src.estimators.volatility import robust_vol_calc

from src.common_utils.utils.column_operations.add_and_populate_column import (
    add_column_and_populate_it_by_value,
)
from src.common_utils.utils.column_operations.rename_columns import rename_columns
from src.common_utils.utils.date_time_operations.date_time_convertions import (
    convert_datetime_to_unixtime,
)
from src.risk.schemas.robust_volatility_schema import RobustVolatilitySchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityService:
    """
    Service for calculating robust volatility of financial instruments.
    """

    def __init__(self):
        self.risk_schema = RobustVolatilitySchema()

    def calculate_volatility_for_instrument(
        self, series: pd.Series, symbol: str
    ) -> pd.DataFrame:
        """
        Calculates the volatility of a given financial instrument represented by a Pandas Series.
        """
        try:
            volatility = robust_vol_calc(series).dropna()
            data_frame = pd.DataFrame(volatility)
            data_frame.reset_index(inplace=True)
            renamed = rename_columns(data_frame, self.risk_schema.columns)
            unix_timed = convert_datetime_to_unixtime(
                renamed, self.risk_schema.index_column
            )
            populated = add_column_and_populate_it_by_value(
                unix_timed, "symbol", symbol
            )
            return populated
        except Exception as error:
            logger.error(
                "Failed to calculate volatility for instrument %s: %s",
                symbol,
                error,
                exc_info=True,
            )
            raise

"""
qwe
"""

import logging

import pandas as pd

from shared.src.estimators.volatility import robust_vol_calc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityService:
    """
    qwe
    """

    def calculate_volatility_for_instrument(self, series: pd.Series):
        """
        qwe
        """
        volatility = robust_vol_calc(series).dropna()
        vol_df = volatility.reset_index()
        vol_df.columns = ["date_time", "volatility"]

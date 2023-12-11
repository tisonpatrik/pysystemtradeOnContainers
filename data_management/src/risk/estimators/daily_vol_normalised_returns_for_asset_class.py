from typing import List

import pandas as pd
from src.core.utils.logging import AppLogger


class DailyVolNormalisedPriceForAssetClassEstimator:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def aggregate_daily_vol_normalised_returns_for_list_of_instruments(
        self,
        aggregated_returns_across_instruments_list: List[pd.Series],
    ) -> pd.Series:
        """
        Average normalised returns across an asset class
        """
        aggregate_returns_across_instruments = pd.concat(
            aggregated_returns_across_instruments_list, axis=1
        )
        # we don't ffill before working out the median as this could lead to
        # bad data
        median_returns = aggregate_returns_across_instruments.median(axis=1)
        norm_price = median_returns.cumsum()

        return norm_price

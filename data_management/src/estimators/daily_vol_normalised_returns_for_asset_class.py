from typing import List

import pandas as pd

from common.logging.logging import AppLogger


class DailyVolNormalisedPriceForAssetClassEstimator:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def aggregate_daily_vol_normalised_returns_for_list_of_instruments(
        self,
        aggregated_returns_across_instruments_list: pd.DataFrame,
    ) -> pd.Series:
        """
        Average normalised returns across an asset class
        """
        # we don't ffill before working out the median as this could lead to
        # bad data
        median_returns = aggregated_returns_across_instruments_list.median(
            axis=1, numeric_only=True
        )
        norm_price = median_returns.cumsum()

        return norm_price

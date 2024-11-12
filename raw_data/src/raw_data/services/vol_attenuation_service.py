from bisect import bisect_left, insort_left

import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger


class VolAttenuationService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_vol_attenuation(self, normalised_vol: pd.Series) -> pd.Series:
        """Calculate the volatility attenuation with quantile-based adjustment and exponential smoothing."""
        try:
            normalised_vol_quantile = self._calculate_quantile_of_points_in_data_series(normalised_vol)
            vol_attenuation = self._multiplier_function(normalised_vol_quantile)
            return vol_attenuation.ewm(span=10).mean()
        except Exception:
            self.logger.exception("Error in calculating volatility attenuation")
            raise

    def _calculate_quantile_of_points_in_data_series(self, normalised_vol: pd.Series) -> pd.Series:
        """Calculate the quantile of each point in the series based on previous values."""
        sorted_values = []
        results = []
        for current_value in normalised_vol:
            position = bisect_left(sorted_values, current_value)
            results.append(position / (len(sorted_values) + 1))
            insort_left(sorted_values, current_value)

        return pd.Series(results, index=normalised_vol.index)

    def _multiplier_function(self, normalised_vol_q: pd.Series) -> pd.Series:
        """Apply a multiplier function based on quantile values."""
        vol_attenuation = np.where(
            np.isnan(normalised_vol_q),
            1.0,
            2 - 1.5 * normalised_vol_q,
        )
        return pd.Series(vol_attenuation, index=normalised_vol_q.index)

import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.utils.quantiles import calculate_quantile_of_points_in_data_series, multiplier_function


class VolAttenuationService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_vol_attenuation(self, normalised_vol: pd.Series) -> pd.Series:
        """Calculate the volatility attenuation with quantile-based adjustment and exponential smoothing."""
        try:
            normalised_vol_quantile = calculate_quantile_of_points_in_data_series(normalised_vol)
            vol_attenuation = multiplier_function(normalised_vol_quantile)
            attenuntation: pd.Series = vol_attenuation.ewm(span=10).mean()
            return attenuntation
        except Exception:
            self.logger.exception("Error in calculating volatility attenuation")
            raise

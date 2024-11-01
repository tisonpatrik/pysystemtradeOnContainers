import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.services.momentum import MomentumService
from rules.src.utils.robust_vol_calc import robust_vol_calc


class SkewabsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.momentum_service = MomentumService()

    def calculate_skewabs(self, demean_factor_value: pd.Series, smooth: int) -> pd.Series:
        try:
            vol = robust_vol_calc(demean_factor_value)
            normalised_factor_value = demean_factor_value / vol
            return normalised_factor_value.ewm(span=smooth).mean()
        except Exception as e:
            self.logger.exception("Error occurred in Skewabs calculation")
            raise ValueError("Failed to compute Skewabs due to invalid inputs or unexpected data issues.") from e

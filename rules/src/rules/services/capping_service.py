import pandas as pd

from common.src.logging.logger import AppLogger
from rules.constants import lower_floor, upper_cap


class CappingService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def apply_capping_to_signal(self, raw_forecast: pd.Series) -> pd.Series:
        try:
            return raw_forecast.clip(upper=upper_cap, lower=lower_floor)

        except Exception as e:
            self.logger.exception("Error occurred in apply_capping_to_signal")
            raise ValueError("Failed to apply capping to signal due to invalid inputs or unexpected data issues.") from e

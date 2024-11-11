import pandas as pd

from common.src.logging.logger import AppLogger


class CarryService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_raw_carry(self, raw_carry: pd.Series, smooth_days: int) -> pd.Series:
        try:
            return raw_carry.ewm(smooth_days).mean()
        except Exception:
            self.logger.exception("An error occurred while calculating raw carry")
            raise ValueError("Failed to calculate raw carry due to an error.") from None

    def calculate_relative_carry(self, smoothed_carry: pd.Series, median_carry_for_asset_class: pd.Series) -> pd.Series:
        try:
            return smoothed_carry - median_carry_for_asset_class
        except Exception:
            self.logger.exception("An error occurred while calculating relative carry")
            raise ValueError("Failed to calculate relative carry due to an error.") from None

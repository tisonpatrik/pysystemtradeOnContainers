import pandas as pd

from common.src.logging.logger import AppLogger


class SmoothCarryService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_smooth_carry(self, raw_carry: pd.Series, smooth_days: int = 90) -> pd.Series:
        try:
            return raw_carry.ewm(smooth_days).mean()
        except Exception:
            self.logger.exception("Unexpected error occurred while calculating Smooth carry")
            raise

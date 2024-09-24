import pandas as pd

from common.src.logging.logger import AppLogger


class CarryService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_raw_carry(self, raw_carry: pd.Series, smooth_days: int) -> pd.Series:
        try:
            return raw_carry.ewm(smooth_days).mean()

        except Exception:
            self.logger.exception("An error occurred")
            raise

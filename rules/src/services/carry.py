import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_root_bdays_inyear


class CarryService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_raw_carry(self, daily_ann_roll: pd.Series, vol: pd.Series) -> pd.Series:
        try:
            ann_stdev = vol * get_root_bdays_inyear()
            return daily_ann_roll / ann_stdev

        except Exception:
            self.logger.exception("An error occurred")
            raise

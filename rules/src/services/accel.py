import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.utils.ewmac import ewmac


class AccelService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_accel(self, price: pd.Series, vol: pd.Series, Lfast: int) -> pd.Series:
        try:
            Lslow = Lfast * 4
            ewmac_signal = ewmac(price, vol, Lfast, Lslow)
            accel = ewmac_signal - ewmac_signal.shift(Lfast)
            return accel

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise

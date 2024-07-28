import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.utils.ewmac import ewmac
from rules.src.utils.robust_vol_calc import robust_vol_calc


class AssettrendService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_assettrend(self, price: pd.Series, Lfast: int) -> pd.Series:
        try:
            Lslow = Lfast * 4
            vol_days = 35
            vol = robust_vol_calc(price, vol_days)
            forecast = ewmac(price, vol, Lfast, Lslow)

            return forecast
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise

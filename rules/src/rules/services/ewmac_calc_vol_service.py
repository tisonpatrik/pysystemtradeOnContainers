import pandas as pd

from common.src.logging.logger import AppLogger
from rules.services.momentum import MomentumService
from rules.utils.robust_vol_calc import robust_vol_calc


class EwmacCalsVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.momentum_service = MomentumService()

    def calculate_ewmac_calc_vol(self, price: pd.Series, lfast: int, lslow: int) -> pd.Series:
        try:
            vol_days = 35
            vol = robust_vol_calc(price, vol_days)

            return self.momentum_service.calculate_ewmac(price, vol, lfast, lslow)
        except Exception as e:
            self.logger.exception("Error occurred in Assettrend calculation")
            raise ValueError("Failed to compute Assettrend due to invalid inputs or unexpected data issues.") from e

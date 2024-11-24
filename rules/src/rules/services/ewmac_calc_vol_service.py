import pandas as pd

from common.logging.logger import AppLogger
from rules.constants import VOL_DAYS
from rules.services.momentum import MomentumService
from rules.utils.robust_vol_calc import robust_vol_calc


class EwmacCalsVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.momentum_service = MomentumService()

    def calculate_ewmac_calc_vol(self, price: pd.Series, lfast: int, lslow: int) -> pd.Series:
        try:
            # Calculate the volatility
            vol = robust_vol_calc(price, VOL_DAYS)
            # Ensure `calculate_ewmac` outputs a pd.Series
            result: pd.Series = self.momentum_service.calculate_ewmac(price, vol, lfast, lslow)
            return result
        except Exception as e:
            self.logger.exception("Error occurred in EWMAC calculation.")
            raise ValueError("Failed to compute EWMAC due to invalid inputs or unexpected data issues.") from e

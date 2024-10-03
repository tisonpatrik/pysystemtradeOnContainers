import pandas as pd

from common.src.logging.logger import AppLogger
from rules.src.services.momentum import MomentumService


class AccelService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.momentum_service = MomentumService()

    def calculate_accel(self, price: pd.Series, vol: pd.Series, Lfast: int) -> pd.Series:
        try:
            ewmac_signal = self.momentum_service.calculate_ewmac(price, vol, Lfast)
            return ewmac_signal - ewmac_signal.shift(Lfast)

        except Exception:
            self.logger.exception("An error occurred")
            raise

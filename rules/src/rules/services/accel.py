import pandas as pd

from common.logging.logger import AppLogger


class AccelService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_accel(self, ewmac_signal: pd.Series, Lfast: int) -> pd.Series:
        try:
            return ewmac_signal - ewmac_signal.shift(Lfast)

        except IndexError:
            self.logger.exception("Index error")
            raise
        except Exception:
            self.logger.exception("An unexpected error occurred")
            raise

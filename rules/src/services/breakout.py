import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger


class BreakoutService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_breakout(self, price: pd.Series, lookback: int) -> pd.Series:
        try:
            smooth = max(int(lookback / 4.0), 1)
            roll_max = price.rolling(lookback, min_periods=int(min(len(price), np.ceil(lookback / 2.0)))).max()
            roll_min = price.rolling(lookback, min_periods=int(min(len(price), np.ceil(lookback / 2.0)))).min()
            roll_mean = (roll_max + roll_min) / 2.0

            # gives a nice natural scaling
            output = 40.0 * ((price - roll_mean) / (roll_max - roll_min))
            return output.ewm(span=smooth, min_periods=np.ceil(smooth / 2.0)).mean()
        except Exception:
            self.logger.exception("Error occurred in breakout calculation")
            raise

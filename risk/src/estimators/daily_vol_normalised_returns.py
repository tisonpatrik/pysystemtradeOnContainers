import pandas as pd
from src.estimators.daily_returns_volatility import DailyReturnsVolEstimator

from common.src.logging.logger import AppLogger


class DailyVolNormalisedReturns:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_estimator = DailyReturnsVolEstimator()

    def get_daily_vol_normalised_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Get returns normalised by recent vol
        Useful statistic, also used for some trading rules
        """
        returnvol = self.daily_returns_vol_estimator.process_daily_returns_vol(
            daily_prices
        ).shift(1)
        dailyreturns = self.daily_returns_vol_estimator.daily_returns(daily_prices)
        norm_return = dailyreturns / returnvol

        return norm_return
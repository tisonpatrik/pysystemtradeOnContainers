import pandas as pd
from src.core.utils.logging import AppLogger
from src.risk.estimators.daily_returns_volatility import DailyReturnsVolEstimator


class CumulativeDailyVolNormalisedReturns:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_vol_processor = DailyReturnsVolEstimator()

    def get_cumulative_daily_vol_normalised_returns(
        self,
        daily_prices: pd.Series,
    ) -> pd.Series:
        """
        Returns a cumulative normalised return. This is like a price, but with equal expected vol
        Used for a few different trading rules
        """

        norm_returns = self.get_daily_vol_normalised_returns(daily_prices)

        cum_norm_returns = norm_returns.cumsum()

        return cum_norm_returns

    def get_daily_vol_normalised_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Get returns normalised by recent vol
        Useful statistic, also used for some trading rules
        """
        returnvol = self.daily_returns_vol_processor.process_daily_returns_vol(
            daily_prices
        ).shift(1)
        dailyreturns = self.daily_returns_vol_processor.daily_returns(daily_prices)
        norm_return = dailyreturns / returnvol

        return norm_return

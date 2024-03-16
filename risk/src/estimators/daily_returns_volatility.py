import pandas as pd

from risk.src.estimators.volatility import mixed_vol_calc


class DailyReturnsVolEstimator:

    def process_daily_returns_vol(self, daily_prices: pd.Series) -> pd.Series:
        price_returns = self.daily_returns(daily_prices)
        vol_multiplier = 1
        raw_vol = mixed_vol_calc(price_returns)

        vol = vol_multiplier * raw_vol
        return vol

    def daily_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Gets daily returns (not % returns)
        """
        dailyreturns = daily_prices.diff()
        return dailyreturns

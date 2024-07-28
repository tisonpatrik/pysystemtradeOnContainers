import pandas as pd

from common.src.utils.volatility import daily_returns, mixed_vol_calc


class DailyVolNormalisedReturns:
    def __init__(self):
        pass

    def get_daily_vol_normalised_returns(self, daily_prices: pd.Series) -> pd.Series:
        """
        Get returns normalised by recent vol
        Useful statistic, also used for some trading rules
        """
        returnvol = self.daily_returns_volatility(daily_prices).shift(1)
        dailyreturns = daily_returns(daily_prices)
        norm_return = dailyreturns / returnvol

        return norm_return

    def daily_returns_volatility(self, daily_prices: pd.Series) -> pd.Series:
        price_returns = daily_returns(daily_prices)
        vol_multiplier = 1
        raw_vol = mixed_vol_calc(price_returns)
        vol = vol_multiplier * raw_vol
        return vol

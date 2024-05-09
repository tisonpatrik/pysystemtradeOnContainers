import pandas as pd

from risk.src.estimators.volatility import mixed_vol_calc


class DailyVolNormalisedReturns:
	def __init__(self):
		pass

	def get_daily_vol_normalised_returns(self, daily_prices: pd.Series) -> pd.Series:
		"""
		Get returns normalised by recent vol
		Useful statistic, also used for some trading rules
		"""
		returnvol = self.process_daily_returns_vol(daily_prices).shift(1)
		dailyreturns = self.daily_returns(daily_prices)
		norm_return = dailyreturns / returnvol

		return norm_return

	def process_daily_returns_vol(self, daily_prices: pd.Series) -> pd.Series:
		price_returns = self.daily_returns(daily_prices)
		vol_multiplier = 1
		raw_vol = mixed_vol_calc(price_returns)
		vol = vol_multiplier * raw_vol
		return vol

	def daily_returns(self, daily_prices: pd.Series) -> pd.Series:
		dailyreturns = daily_prices.diff()
		return dailyreturns

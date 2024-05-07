from datetime import datetime

import numpy as np
import pandas as pd

from common.src.logging.logger import AppLogger


class FxService:
	def __init__(self):
		self.default_currency = 'USD'
		self.logger = AppLogger.get_instance().get_logger()

	def get_default_rate_series(self, start_date='1970-01-01') -> pd.Series:
		try:
			end_date = datetime.now()
			default_rate = 1.0
			dates = pd.date_range(start=start_date, freq='B', end=end_date)
			rate_series = pd.Series(np.full(len(dates), default_rate), index=dates)
			return rate_series
		except Exception as e:
			self.logger.error(f'Failed to generate default rate series: {e}')
			raise

	def calculate_inversion(self, fx_prices: pd.Series) -> pd.Series:
		try:
			return 1.0 / fx_prices
		except Exception as e:
			self.logger.error(f'Error inverting FX prices: {e}')
			raise

	def calculate_fx_cross(self, fx_prices1: pd.Series, fx_prices2: pd.Series) -> pd.Series:
		try:
			(aligned_c1, aligned_c2) = fx_prices1.align(fx_prices2, join='outer')
			fx_rate_series = aligned_c1.ffill() / aligned_c2.ffill()
			return fx_rate_series.dropna()
		except Exception as e:
			self.logger.error(f'Error calculating FX cross rate: {e}')
			raise

import pandas as pd

from common.src.logging.logger import AppLogger


class CumulativeDailyVolatilityNormalisedReturnsService:
	def __init__(self):
		self.logger = AppLogger.get_instance().get_logger()

	def calculate_cumulative_vol_for_prices(self, daily_vol_normalised_returns: pd.DataFrame) -> pd.DataFrame:
		"""
		Calculate cumulative returns volatility by symbol and returns them as Pandas Series.
		"""
		try:
			# SELECT id, hodnota, SUM(hodnota) OVER (ORDER BY id) AS cumsum FROM   tabulka;
			cum_norm_returns = daily_vol_normalised_returns.cumsum()
			cum_norm_returns = cum_norm_returns.rename(columns={'vol_normalized_returns': 'cum_vol_norm_returns'})
			return cum_norm_returns

		except Exception as error:
			error_message = f'An error occurred during the processing: {error}'
			self.logger.error(error_message)
			raise ValueError(error_message)

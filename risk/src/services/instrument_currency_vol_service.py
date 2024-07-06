import pandas as pd

from common.src.logging.logger import AppLogger


class InstrumentCurrencyVolService:
	def __init__(self):
		self.logger = AppLogger.get_instance().get_logger()

	def calculate_instrument_vol_async(
		self, denom_price: pd.Series, daily_returns_vol: pd.Series, point_size: float
	) -> pd.Series:
		""" """
		try:
			block_value = self.get_block_value(denom_price, point_size)
			daily_perc_vol = self.get_daily_percentage_volatility(denom_price, daily_returns_vol)
			## FIXME WHY NOT RESAMPLE?
			(block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join='inner')

			instr_ccy_vol = block_value.ffill() * daily_perc_vol
			return instr_ccy_vol

		except Exception as error:
			error_message = f'An error occurred during the processing: {error}'
			self.logger.error(error_message)
			raise ValueError(error_message)

	def get_block_value(self, denom_price: pd.Series, value_of_price_move: float) -> pd.Series:
		block_value = denom_price.ffill() * value_of_price_move * 0.01
		return block_value

	def get_daily_percentage_volatility(self, denom_price: pd.Series, daily_returns_vol: pd.Series) -> pd.Series:
		# Calculate the volatility of daily returns
		(denom_price, return_vol) = denom_price.align(daily_returns_vol, join='right')
		perc_vol = 100.0 * (return_vol / denom_price.ffill().abs())
		return perc_vol

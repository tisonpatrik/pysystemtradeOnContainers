import pandas as pd

from common.src.logging.logger import AppLogger
from risk.src.estimators.daily_vol_normalised_returns_for_asset_class import (
	DailyVolNormalisedPriceForAssetClassEstimator,
)


class DailyVolNormalisedPriceForAssetClassService:
	def __init__(self):
		self.logger = AppLogger.get_instance().get_logger()
		self.estimator = DailyVolNormalisedPriceForAssetClassEstimator()

	def calculate_daily_vol_normalised_price_for_asset_class(
		self, returns_across_instruments_list: pd.DataFrame
	) -> pd.Series:
		try:
			pivot_df = returns_across_instruments_list.pivot_table(
				index='date_time', columns='symbol', values='vol_normalized_returns'
			)

			daily_returns_vols = self.estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(pivot_df)
			cleaned = daily_returns_vols.dropna()
			return cleaned

		except Exception as error:
			error_message = f'An error occurred during the processing: {error}'
			self.logger.error(error_message)
			raise ValueError(error_message)

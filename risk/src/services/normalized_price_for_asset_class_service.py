import pandas as pd

from common.src.logging.logger import AppLogger


class normalizedPriceForAssetClassService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_cumulative_daily_vol_normalized_returns(
        self, normalized_price_for_asset_class: pd.Series, normalized_price_this_instrument: pd.Series
    ) -> pd.Series:
        try:
            normalized_price_for_asset_class_aligned = normalized_price_for_asset_class.reindex(
                normalized_price_this_instrument.index
            ).ffill()
            return normalized_price_for_asset_class_aligned
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while calculating Cumulative Daily volatility normalized returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

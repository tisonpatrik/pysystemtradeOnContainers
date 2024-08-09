import pandas as pd

from common.src.logging.logger import AppLogger


class NormalisedPriceForAssetClassService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_cumulative_daily_vol_normalised_returns(
        self, normalised_price_for_asset_class: pd.Series, normalised_price_this_instrument: pd.Series
    ) -> pd.Series:
        try:
            normalised_price_for_asset_class_aligned = normalised_price_for_asset_class.reindex(
                normalised_price_this_instrument.index
            ).ffill()
            return normalised_price_for_asset_class_aligned
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while calculating Cumulative Daily volatility normalised returns: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

import pandas as pd

from common.src.logging.logger import AppLogger


class normalizedPriceForAssetClassService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_cumulative_daily_vol_normalized_returns(
        self, normalized_price_for_asset_class: pd.Series, normalized_price_this_instrument: pd.Series
    ) -> pd.Series:
        try:
            return normalized_price_for_asset_class.reindex(normalized_price_this_instrument.index).ffill()
        except Exception:
            self.logger.exception("Unexpected error occurred while calculating Cumulative Daily volatility normalized returns")
            raise

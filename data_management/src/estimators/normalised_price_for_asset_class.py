import pandas as pd

from common.src.logging.logger import AppLogger


class NormalisedPriceForAssetClass:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_normalised_price_for_asset_class(
        self,
        instrument_cumulative_normalised_price: pd.Series,
        normalised_price_for_asset_class: pd.Series,
    ) -> pd.Series:
        """
        Aligns and forward-fills the normalised price series with the cumulative
        normalised price index to calculate daily volatility-normalised returns for an asset class.
        """
        normalised_price_for_asset_class_aligned = (
            normalised_price_for_asset_class.reindex(
                index=instrument_cumulative_normalised_price.index
            ).ffill()
        )

        return normalised_price_for_asset_class_aligned

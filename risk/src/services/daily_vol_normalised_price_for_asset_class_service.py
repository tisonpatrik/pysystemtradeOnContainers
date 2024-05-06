from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from risk.src.estimators.daily_vol_normalised_returns_for_asset_class import (
    DailyVolNormalisedPriceForAssetClassEstimator,
)
from risk.src.schemas.risk_schemas import DailyVolNormalizedReturnsSchema, Volatility


class DailyVolNormalisedPriceForAssetClassService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyVolNormalisedPriceForAssetClassEstimator()

    def calculate_daily_vol_normalised_price_for_asset_class(
        self, returns_across_instruments_list: DataFrame[DailyVolNormalizedReturnsSchema]
    ) -> Series[Volatility]:
        """ """
        try:
            pivot_df = returns_across_instruments_list.pivot(
                index=DailyVolNormalizedReturnsSchema.date_time,
                columns="symbol",
                values=DailyVolNormalizedReturnsSchema.vol_normalized_returns,
            )

            daily_returns_vols = self.estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(pivot_df)
            cleaned = daily_returns_vols.dropna()
            return Series[Volatility](cleaned)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

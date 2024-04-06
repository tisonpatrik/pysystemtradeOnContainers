import pandas as pd
from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.daily_vol_normalised_returns_for_asset_class import (
    DailyVolNormalisedPriceForAssetClassEstimator,
)
from risk.src.models.risk_models import DailyVolNormalisedPriceForAssetClassModel
from risk.src.schemas.risk_schemas import (
    DailyVolNormalisedPriceForAssetClassSchema,
    DailyVolNormalizedReturnsSchema,
    Volatility,
)


class DailyVolNormalisedPriceForAssetClassService:
    def __init__(self, repository: Repository[DailyVolNormalisedPriceForAssetClassModel]):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyVolNormalisedPriceForAssetClassEstimator()

    async def insert_daily_vol_normalised_price_for_asset_class_async(
        self, daily_returns_vols: Series[Volatility], asset: str
    ):
        """
        Insert daily volatility normalised price for asset class.
        """
        try:

            framed = convert_series_to_frame(daily_returns_vols)
            populated = add_column_and_populate_it_by_value(
                framed, DailyVolNormalisedPriceForAssetClassSchema.asset_class, asset
            )
            renamed = rename_columns(
                populated,
                [
                    DailyVolNormalisedPriceForAssetClassSchema.date_time,
                    DailyVolNormalisedPriceForAssetClassSchema.normalized_volatility,
                    DailyVolNormalisedPriceForAssetClassSchema.asset_class,
                ],
            )
            validated = DataFrame[DailyVolNormalisedPriceForAssetClassSchema](renamed)
            await self.repository.insert_dataframe_async(validated)

        except Exception as error:
            error_message = f"An error occurred during the processing for asset '{asset}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def calculate_daily_vol_normalised_price_for_asset_class_async(
        self, returns_across_instruments_list: list[Series[Volatility]]
    ) -> Series[Volatility]:
        """ """
        try:
            aggregated_returns_across_instruments_list = pd.concat(returns_across_instruments_list, axis=1, sort=True)
            daily_returns_vols = self.estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(
                aggregated_returns_across_instruments_list
            )
            cleaned = daily_returns_vols.dropna()
            return Series[Volatility](cleaned)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)



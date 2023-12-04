from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.risk.errors.normalised_price_for_asset_class_error import (
    DailyNormalisedPriceForAssetClassFetchError,
)
from src.risk.models.risk_models import DailyVolNormalisedPriceForAssetClass


class DailyVolNormalisedPriceForAssetClassService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_loader_service = DataLoadService(db_session)
        self.table_name = DailyVolNormalisedPriceForAssetClass.__tablename__
        self.time_column = DailyVolNormalisedPriceForAssetClass.unix_date_time.key
        self.price_column = (
            DailyVolNormalisedPriceForAssetClass.normalized_volatility.key
        )

    async def get_daily_vol_normalised_price_for_asset_class_async(
        self, asset_class: str
    ):
        """
        Asynchronously fetches daily normalised price for asset class by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, asset_class
            )
            converted_and_sorted = convert_and_sort_by_time(data, self.time_column)
            series = convert_frame_to_series(
                converted_and_sorted, self.time_column, self.price_column
            )
            return series
        except Exception as exc:
            self.logger.error(
                "Failed to get daily returns volatility asynchronously: %s",
                exc,
                exc_info=True,
            )
            raise DailyNormalisedPriceForAssetClassFetchError(asset_class, exc)

from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.polars.prapare_db_calculations import prepara_asset_data_to_db
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.db.services.data_load_service import DataLoadService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.normalised_price_for_asset_class_error import (
    DailyNormalisedPriceForAssetCalculationError,
    DailyNormalisedPriceForAssetClassFetchError,
)
from src.risk.estimators.daily_vol_normalised_returns_for_asset_class import (
    DailyVolNormalisedPriceForAssetClassEstimator,
)
from src.risk.models.risk_models import DailyVolNormalisedPriceForAssetClass
from src.risk.services.daily_volatility_normalised_returns_service import (
    DailyVolatilityNormalisedReturnsService,
)


class DailyVolNormalisedPriceForAssetClassService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.data_loader_service = DataLoadService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.daily_volatility_normalised_returns_service = (
            DailyVolatilityNormalisedReturnsService(db_session)
        )
        self.daily_vol_normalised_returns_for_asset_class_estimator = (
            DailyVolNormalisedPriceForAssetClassEstimator()
        )
        self.table_name = DailyVolNormalisedPriceForAssetClass.__tablename__
        self.time_column = DailyVolNormalisedPriceForAssetClass.unix_date_time.key
        self.price_column = (
            DailyVolNormalisedPriceForAssetClass.normalized_volatility.key
        )

    async def insert_daily_vol_normalised_price_for_asset_class_async(
        self, asset_class
    ):
        """
        Calculates and insert daily normalised price for asset class.
        """
        try:
            list_of_instruments = await self.instrument_config_service.get_instruments_by_asset_class_async(
                asset_class
            )
            aggregate_returns_across_instruments_list = []
            for instrument_code in list_of_instruments:
                normalised_returns = await self.daily_volatility_normalised_returns_service.get_daily_vol_normalised_returns_async(
                    instrument_code
                )
                aggregate_returns_across_instruments_list.append(normalised_returns)

            returns = self.daily_vol_normalised_returns_for_asset_class_estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(
                aggregate_returns_across_instruments_list
            )
            prepared_data = prepara_asset_data_to_db(
                returns, DailyVolNormalisedPriceForAssetClass, asset_class
            )
            # await self.data_insert_service.async_insert_dataframe_to_table(
            #     prepared_data, self.table_name
            # )
        except Exception as exc:
            self.logger.error(
                f"Error in calculating cumulative volatility returns: {exc}"
            )
            raise DailyNormalisedPriceForAssetCalculationError()

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

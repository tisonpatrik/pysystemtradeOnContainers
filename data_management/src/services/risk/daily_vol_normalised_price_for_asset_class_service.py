import pandas as pd
from src.app.schemas.risk_schemas import DailyVolNormalisedPriceForAssetClassSchema
from src.core.pandas.prapare_db_calculations import prepare_asset_data_to_db
from src.estimators.daily_vol_normalised_returns_for_asset_class import DailyVolNormalisedPriceForAssetClassEstimator
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.services.risk.daily_volatility_normalised_returns_service import DailyVolatilityNormalisedReturnsService
from src.utils.table_operations import sort_by_time

from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from risk.src.models.risk_models import DailyVolNormalisedPriceForAssetClassModel

table_name = DailyVolNormalisedPriceForAssetClassModel.__tablename__


class DailyVolNormalisedPriceForAssetClassService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.daily_volatility_normalised_returns_service = DailyVolatilityNormalisedReturnsService(db_session)
        self.daily_vol_normalised_returns_for_asset_class_estimator = DailyVolNormalisedPriceForAssetClassEstimator()
        self.time_column = DailyVolNormalisedPriceForAssetClassModel.date_time
        self.price_column = DailyVolNormalisedPriceForAssetClassModel.normalized_volatility

    async def insert_daily_vol_normalised_price_for_asset_class_async(self, asset_class):
        """
        Calculates and insert daily normalised price for asset class.
        """
        try:
            list_of_instruments = await self.instrument_config_service.get_instruments_by_asset_class_async(asset_class)
            aggregate_returns_across_instruments_list = []
            # for instrument_code in list_of_instruments:
            #     normalised_returns = await self.daily_volatility_normalised_returns_service.get_daily_vol_normalised_returns_async(
            #         instrument_code
            #     )
            #     aggregate_returns_across_instruments_list.append(normalised_returns)
            # aggregated_returns_across_instruments_list = pd.concat(
            #     aggregate_returns_across_instruments_list, axis=1, sort=True
            # )
            # returns = self.daily_vol_normalised_returns_for_asset_class_estimator.aggregate_daily_vol_normalised_returns_for_list_of_instruments(
            #     aggregated_returns_across_instruments_list
            # )
            # prepared_data = prepare_asset_data_to_db(
            #     returns, DailyVolNormalisedPriceForAssetClass, asset_class
            # )
            # await self.repository.insert_data_async(
            #     prepared_data, DailyVolNormalisedPriceForAssetClassSchema
            # )
            print("neco")
        except Exception as exc:
            error_message = f"Error in calculating daily normalised price for asset class '{asset_class}': {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_vol_normalised_price_for_asset_class_async(self, asset_class: str):
        """
        Asynchronously fetches daily normalised price for asset class by symbol and returns them as Pandas Series.
        """
        try:
            # data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
            #     table_name, asset_class
            # )
            # converted_and_sorted = sort_by_time(data, self.time_column)
            # series = convert_frame_to_series(
            #     converted_and_sorted, self.time_column, self.price_column
            # )
            # return series
            print("neco")

        except Exception as exc:
            error_message = f"Failed to get daily normalized price for asset class '{asset_class}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

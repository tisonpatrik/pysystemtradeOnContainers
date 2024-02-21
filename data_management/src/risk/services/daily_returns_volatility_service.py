"""Module for calculating robust volatility for financial instruments."""

from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.polars.prapare_db_calculations import prepara_data_to_db
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.db.services.data_load_service import DataLoadService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from src.risk.models.risk_models import DailyReturnsVolatility


class DailyReturnsVolService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_loader_service = DataLoadService(db_session)
        self.data_insert_service = DataInsertService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.table_name = DailyReturnsVolatility.__tablename__
        self.price_column = DailyReturnsVolatility.daily_returns_volatility.key
        self.time_column = DailyReturnsVolatility.unix_date_time.key
        self.daily_returns_vol_estimator = DailyReturnsVolEstimator()

    async def insert_daily_returns_vol_for_prices_async(self, prices, symbol):
        """
        Calculates and insert daily returns volatility of a given prices.
        """
        try:
            self.logger.info(
                "Starting the daily returns volatility calculation for %s symbol.",
                symbol,
            )
            daily_returns_vols = (
                self.daily_returns_vol_estimator.process_daily_returns_vol(prices)
            )
            prepared_data = prepara_data_to_db(
                daily_returns_vols, DailyReturnsVolatility, symbol
            )

            await self.data_insert_service.async_insert_dataframe_to_table(
                prepared_data, self.table_name
            )
        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_returns_volatility_async(self, symbol: str):
        """
        Asynchronously fetches daily returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, symbol
            )
            converted_and_sorted = convert_and_sort_by_time(data, self.time_column)
            series = convert_frame_to_series(
                converted_and_sorted, self.time_column, self.price_column
            )
            return series
        except Exception as exc:
            error_message = f"Failed to get daily returns volatility asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

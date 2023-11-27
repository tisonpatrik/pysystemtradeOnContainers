"""Module for calculating robust volatility for financial instruments."""

from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.utils.data_aggregators import concatenate_data_frames
from src.risk.errors.daily_returns_vol_processing_error import (
    DailyReturnsVolatilityFetchError,
    DailyReturnsVolCalculationError,
)
from src.risk.processing.daily_returns_volatility_processing import (
    DailyReturnsVolatilityCalculator,
)
from src.risk.models.risk_models import DailyReturnsVolatility


class DailyReturnsVolatilityService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_loader_service = DataLoadService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.table_name = DailyReturnsVolatility.__tablename__
        self.price_column = DailyReturnsVolatility.daily_returns_volatility.key
        self.time_column = DailyReturnsVolatility.unix_date_time.key
        self.daily_returns_vol_calculator = DailyReturnsVolatilityCalculator(db_session)

    async def calculate_daily_returns_volatility_for_instrument_async(self, model):
        """
        Calculates daily returns volatility of a given financial instrument represented.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)
            # Fetch instrument configurations
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs()
            )
            processed_volatilities = (
                await self.daily_returns_vol_calculator.get_daily_returns_vols_async(
                    instrument_configs, model
                )
            )
            daily_returns_vols = concatenate_data_frames(processed_volatilities)
            return daily_returns_vols
        except DailyReturnsVolCalculationError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise

    async def get_daily_returns_volatility_async(self, symbol: str):
        """
        Asynchronously fetches daily returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                self.table_name, symbol
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
            raise DailyReturnsVolatilityFetchError(symbol, exc)

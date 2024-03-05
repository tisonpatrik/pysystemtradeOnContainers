"""Module for calculating robust volatility for financial instruments."""

from src.app.models.risk_models import DailyReturnsVolatility
from src.app.schemas.risk_schemas import DailyReturnsVolatilitySchema
from src.core.pandas.prapare_db_calculations import prepara_data_to_db
from src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.utils.converter import convert_frame_to_series
from src.utils.table_operations import sort_by_time

from common.src.logging.logger import AppLogger

table_name = DailyReturnsVolatility.__tablename__


class DailyReturnsVolService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.price_column = DailyReturnsVolatility.daily_returns_volatility.key
        self.time_column = DailyReturnsVolatility.date_time.key
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
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

            # await self.repository.insert_data_async(
            #     prepared_data, DailyReturnsVolatilitySchema
            # )
            print("neco")
        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_returns_volatility_async(self, symbol: str):
        """
        Asynchronously fetches daily returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            # data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
            #     table_name, symbol
            # )
            # converted_and_sorted = sort_by_time(data, self.time_column)
            # series = convert_frame_to_series(
            #     converted_and_sorted, self.time_column, self.price_column
            # )
            # return series
            print("neco")

        except Exception as exc:
            error_message = f"Failed to get daily returns volatility asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

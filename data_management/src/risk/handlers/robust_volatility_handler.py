"""
This module defines a handler class for inserting robust volatility data into a database.
It makes use of DataLoadService for database operations and DateTimeService for date-time data handling.
"""
import logging

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from shared.src.db.services.data_insert_service import DataInsertService
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.services.robust_volatility_service import RobustVolatilityService
from src.core.models.risk_schemas import RobustVolatility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    Handler class responsible for inserting robust volatility data into the database.
    Utilizes DataLoadService for database-related operations and DateTimeService for date-time data manipulation.
    """

    def __init__(self, db_session):
        self.db_session = db_session
        self.robust_volatility_service = RobustVolatilityService()
        self.data_inserter = DataInsertService(db_session)
        self.adjusted_service = AdjustedPricesService(self.db_session)

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table,
        performs date-time conversion, and inserts robust volatility data.
        """
        try:
            series_dict = await self.adjusted_service.get_adjusted_prices_async()
            concatenated_data_frame = await self._process_volatility_data(series_dict)
            await self.data_inserter.async_insert_dataframe_to_table(
                concatenated_data_frame, RobustVolatility.__tablename__
            )
        except Exception as error:
            logger.error("Failed to insert robust volatility data: %s", error)
            raise

    async def _process_volatility_data(self, series_dict):
        """
        Processes volatility data for various financial instruments.
        """
        try:
            processed_data_frames = [
                self.robust_volatility_service.calculate_robust_volatility_for_instrument(
                    series, symbol
                )
                for symbol, series in series_dict.items()
            ]

            return concatenate_data_frames(processed_data_frames)
        except Exception as error:
            logger.error("Failed to process volatility data: %s", error)
            raise

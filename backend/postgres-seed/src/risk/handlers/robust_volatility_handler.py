"""
This module defines a handler class for inserting robust volatility data into a database.
It makes use of DataLoadService for database operations and DateTimeService for date-time data handling.
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.data_load_service import DataLoadService
from src.data_processor.services.date_time_service import DateTimeService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    Handler class responsible for inserting robust volatility data into the database.
    Utilizes DataLoadService for database-related operations and DateTimeService for date-time data manipulation.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_load_service = DataLoadService(db_session)
        self.data_time_service = DateTimeService()
        self.source_table = "adjusted_prices"

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table, performs date-time conversion,
        and returns a Pandas Series containing the robust volatility data.
        """
        data_frames = await self.data_load_service.fetch_all_from_table_to_dataframe(
            self.source_table
        )

        series = self.data_time_service.covert_dataframe_to_list_of_series(
            data_frames, "symbol", "unix_date_time"
        )
        # return series

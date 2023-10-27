"""
bla bla
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.data_load_service import DataLoadService
from src.data_processor.services.date_time_service import DateTimeService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    bla bla
    """

    def __init__(self, db_session: AsyncSession):
        self.data_load_service = DataLoadService(db_session)
        self.data_time_service = DateTimeService()
        self.table_name = "adjusted_prices"
        self.datetime_column = "unix_date_time"

    async def insert_robust_volatility_async(self):
        """
        bla bla
        """
        data_frames = await self.data_load_service.fetch_all_from_table_to_dataframe(
            self.table_name
        )
        series = self.data_time_service.convert_raw_dataframe_to_series(
            data_frames, self.datetime_column
        )
        return series

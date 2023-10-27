"""
bla bla
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.services.data_load_service import DataLoadService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    bla bla
    """

    def __init__(self, db_session: AsyncSession):
        self.data_load_service = DataLoadService(db_session)
        self.table_name = "adjusted_prices"

    async def insert_robust_volatility_async(self):
        """
        bla bla
        """
        data_frames = await self.data_load_service.fetch_all_from_table_to_dataframe(
            self.table_name
        )

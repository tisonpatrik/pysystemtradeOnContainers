"""
This module provides services for fetching and processing fx prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.entity_repository import EntityRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import FxPrices

table_name = FxPrices.__tablename__


class FxPricesService:
    """
    Service for dealing with operations related to fx prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = EntityRepository(db_session, FxPrices)

    async def insert_fx_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert fx prices data into db.
        """
        try:
            # await self.repository.insert_records_async(raw_data, table_name)
            print("neco")

        except Exception as exc:
            self.logger.error(f"Error inserting data for {table_name}: {str(exc)}")

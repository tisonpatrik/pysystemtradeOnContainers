"""
This module provides services for fetching and processing fx prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.raw_data_models import FxPricesModel
from src.app.schemas.raw_data_schemas import FxPricesSchema

from common.database.repositories.records_repository import RecordsRepository
from common.logging.logger import AppLogger

table_name = FxPricesModel.__tablename__


class FxPricesService:
    """
    Service for dealing with operations related to fx prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = RecordsRepository(
            db_session=db_session, series_schema=FxPricesSchema
        )

    async def insert_fx_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert fx prices data into db.
        """
        try:
            await self.repository.insert_records_async(raw_data, table_name)

        except Exception as exc:
            self.logger.error(f"Error inserting data for {table_name}: {str(exc)}")

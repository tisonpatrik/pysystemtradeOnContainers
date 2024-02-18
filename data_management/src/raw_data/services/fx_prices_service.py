"""
This module provides services for fetching and processing fx prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.raw_data.models.raw_data_models import FxPricesModel
from src.raw_data.schemas.raw_data_schemas import FxPricesSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


class FxPricesService:
    """
    Service for dealing with operations related to fx prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = FxPricesModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def insert_fx_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert fx prices data into db.
        """
        try:
            await self.data_insertion_service.insert_data(raw_data, FxPricesSchema)

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

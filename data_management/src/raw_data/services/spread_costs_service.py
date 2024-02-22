"""
This module provides services for fetching and processing spread costs data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.config_models import SpreadCostsModel
from src.core.utils.logging import AppLogger
from src.raw_data.schemas.config_schemas import SpreadCostsSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


class SpreadCostService:
    """
    Service for dealing with operations related to spread costs.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = SpreadCostsModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def insert_spread_costs_async(self, raw_data: pd.DataFrame):
        """
        Insert spread costs data into db.
        """
        try:
            await self.data_insertion_service.insert_data(raw_data, SpreadCostsSchema)

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

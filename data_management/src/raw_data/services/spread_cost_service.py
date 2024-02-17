"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

from typing import List

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.raw_data.models.config_models import SpreadCostModel
from src.raw_data.schemas.config_schemas import SpreadCostSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


class SpreadCostService:
    """
    Service for dealing with operations related to spread cost.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = SpreadCostModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    def get_names_of_columns(self) -> List[str]:
        """
        Get names of columns in instrument config table.
        """
        return [column.name for column in SpreadCostModel.__table__.columns]

    async def insert_spread_cost_async(self, raw_data: pd.DataFrame):
        """
        Insert spread cost data into db.
        """
        try:
            await self.data_insertion_service.insert_data(raw_data, SpreadCostSchema)

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

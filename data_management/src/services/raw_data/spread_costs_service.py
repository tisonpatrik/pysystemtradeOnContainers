"""
This module provides services for fetching and processing spread costs data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.config_models import SpreadCostsModel
from src.app.schemas.config_schemas import SpreadCostsSchema

from common.src.logging.logger import AppLogger

table_name = SpreadCostsModel.__tablename__


class SpreadCostService:
    """
    Service for dealing with operations related to spread costs.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_spread_costs_async(self, raw_data: pd.DataFrame):
        """
        Insert spread costs data into db.
        """
        try:
            # await self.data_insertion_service.insert_data_async(
            #     raw_data, SpreadCostsSchema
            # )
            print("neco")

        except Exception as exc:
            self.logger.error(f"Error inserting data for {table_name}: {str(exc)}")

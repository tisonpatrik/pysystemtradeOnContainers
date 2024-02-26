"""
This module provides services for fetching and processing roll calendars data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.raw_data_models import RollCalendarsModel
from src.app.schemas.raw_data_schemas import RollCalendarsSchema
from src.services.data_insertion_service import GenericDataInsertionService

from common.logging.logging import AppLogger


class RollCalendarsService:
    """
    Service for dealing with operations related to roll calendars.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = RollCalendarsModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def insert_roll_calendars_async(self, raw_data: pd.DataFrame):
        """
        Insert roll calendars prices data into db.
        """
        try:
            await self.data_insertion_service.insert_data_async(
                raw_data, RollCalendarsSchema
            )

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

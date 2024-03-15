"""
This module provides services for fetching and processing roll calendars data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import RollCalendars
from raw_data.src.schemas.raw_data_schemas import RollCalendarsSchema

table_name = RollCalendars.__tablename__


class RollCalendarsService:
    """
    Service for dealing with operations related to roll calendars.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_roll_calendars_async(self, raw_data: pd.DataFrame):
        """
        Insert roll calendars prices data into db.
        """
        try:
            # await self.data_insertion_service.insert_data_async(
            #     raw_data, RollCalendarsSchema
            # )
            print("neco")

        except Exception as exc:
            self.logger.error(f"Error inserting data for {table_name}: {str(exc)}")

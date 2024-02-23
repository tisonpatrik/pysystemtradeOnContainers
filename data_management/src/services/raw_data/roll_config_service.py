"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.config_models import RollConfigModel
from src.app.schemas.config_schemas import RollConfigSchema
from src.db.services.data_load_service import DataLoadService
from src.services.data_insertion_service import GenericDataInsertionService

from common.logging.logging import AppLogger


class RollConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = RollConfigModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def get_instrument_configs(self):
        """
        Asynchronously fetch instrument config data.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_async(
                self.table_name
            )
            return data

        except Exception as error:
            error_message = (
                f"Failed to get instrument config table asynchronously: {error}"
            )
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def insert_roll_config_async(self, raw_data: pd.DataFrame):
        """
        Insert roll config data into db.
        """
        try:
            await self.data_insertion_service.insert_data(raw_data, RollConfigSchema)

        except Exception as exc:
            error_message = f"Error inserting data for {self.table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

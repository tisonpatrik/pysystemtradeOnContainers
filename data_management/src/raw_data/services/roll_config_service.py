"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import InstrumentConfigError
from src.raw_data.models.config_models import RollConfigModel
from src.raw_data.schemas.config_schemas import RollConfigSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


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
            self.logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument config", error)

    async def insert_roll_config_async(self, raw_data: pd.DataFrame):
        """
        Insert roll config data into db.
        """
        try:
            await self.data_insertion_service.insert_data(raw_data, RollConfigSchema)

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

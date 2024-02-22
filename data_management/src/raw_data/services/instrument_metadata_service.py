"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.config_models import InstrumentMetadataModel
from src.app.schemas.config_schemas import InstrumentMetadataSchema
from src.core.utils.logging import AppLogger
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


class InstrumentMetadataService:
    """
    Service for dealing with operations related to instrument metadata.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = InstrumentMetadataModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def insert_instruments_metadata_async(self, raw_data: pd.DataFrame):
        """
        Insert instruments metadata data into db.
        """
        try:
            await self.data_insertion_service.insert_data(
                raw_data, InstrumentMetadataSchema
            )

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

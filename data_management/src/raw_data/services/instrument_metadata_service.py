"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

from typing import List

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.raw_data.models.config_models import InstrumentMetadataModel
from src.raw_data.schemas.config_schemas import InstrumentMetadataSchema
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

    def get_names_of_columns(self) -> List[str]:
        """
        Get names of columns in instrument config table.
        """
        return [column.name for column in InstrumentMetadataModel.__table__.columns]

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

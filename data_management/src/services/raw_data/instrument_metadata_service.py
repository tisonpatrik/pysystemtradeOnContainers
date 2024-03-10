"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentMetadata
from raw_data.src.schemas.config_schemas import InstrumentMetadataSchema

table_name = InstrumentMetadata.__tablename__


class InstrumentMetadataService:
    """
    Service for dealing with operations related to instrument metadata.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()

    async def insert_instruments_metadata_async(self, raw_data: pd.DataFrame):
        """
        Insert instruments metadata data into db.
        """
        try:
            # await self.data_insertion_service.insert_data_async(
            #     raw_data, InstrumentMetadataSchema
            # )
            print("neco")

        except Exception as exc:
            self.logger.error(f"Error inserting data for {table_name}: {str(exc)}")

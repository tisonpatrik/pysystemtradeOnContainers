"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from raw_data.src.models.config_models import InstrumentConfigModel
from raw_data.src.schemas.config_schemas import InstrumentConfigSchema

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger

table_name = InstrumentConfigModel.__tablename__


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(
            db_session=db_session, entity_class=InstrumentConfigModel
        )

    async def get_instrument_configs_async(self):
        """
        Asynchronously fetch instrument consfig data.
        """
        try:
            data = await self.repository.get_all_async()
            print("neco")
        except Exception as error:
            error_message = f"Failed to get instrument config asynchronously for table '{table_name}': {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_point_size_of_instrument_async(self, symbol):
        """Asynchronously fetch point size for given instrument."""
        try:
            data = await self.repository.get_all_async()
            # return data[InstrumentConfigSchema.pointsize][0]
        except Exception as error:
            error_message = f"Failed to get point size for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_assets_class_by_symbol_async(self, symbol):
        """
        Asynchronously fetch instrument metadatas.
        """
        try:
            data = await self.repository.get_all_async()
            print("neco")

        except Exception as error:
            error_message = f"Failed to get instrument metadatas for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_instruments_by_asset_class_async(self, asset_class):
        """
        Asynchronously fetch instrument aset class.
        """
        try:
            data = await self.repository.get_all_async()
            print("neco")

        except Exception as error:
            error_message = f"Failed to get instruments by asset class '{asset_class}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_assets_async(self):
        """
        Asynchronously fetch instrument config data.
        """
        try:
            data = await self.repository.get_all_async()
            print("neco")
        except Exception as error:
            error_message = f"Failed to get assets values asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def insert_instruments_config_async(self, raw_data: pd.DataFrame):
        """
        Insert instruments config data into db.
        """
        try:
            print("neco")

        except Exception as exc:
            error_message = f"Error inserting data for {table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

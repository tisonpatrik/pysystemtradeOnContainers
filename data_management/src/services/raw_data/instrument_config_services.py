"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.config_models import InstrumentConfigModel
from src.app.schemas.config_schemas import InstrumentConfigSchema
from src.db.services.data_load_service import DataLoadService
from src.services.data_insertion_service import GenericDataInsertionService

from common.logging.logging import AppLogger


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = InstrumentConfigModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def get_instrument_configs_async(self):
        """
        Asynchronously fetch instrument config data.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_async(
                self.table_name
            )
            return data
        except Exception as error:
            error_message = f"Failed to get instrument config asynchronously for table '{self.table_name}': {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_point_size_of_instrument_async(self, symbol):
        """Asynchronously fetch point size for given instrument."""
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, symbol
            )
            return data[InstrumentConfigSchema.pointsize][0]
        except Exception as error:
            error_message = f"Failed to get point size for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_assets_class_by_symbol_async(self, symbol):
        """
        Asynchronously fetch instrument metadatas.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, symbol
            )
            return data[InstrumentConfigSchema.asset_class][0]

        except Exception as error:
            error_message = f"Failed to get instrument metadatas for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_instruments_by_asset_class_async(self, asset_class):
        """
        Asynchronously fetch instrument aset class.
        """
        try:
            data = await self.data_loader_service.fetch_rows_by_column_value_async(
                table_name=self.table_name,
                column_name=InstrumentConfigSchema.asset_class,
                column_value=asset_class,
            )
            return data[InstrumentConfigSchema.symbol]

        except Exception as error:
            error_message = f"Failed to get instruments by asset class '{asset_class}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def get_unique_values_for_given_column_from_instrumnet_config(
        self, column_name
    ):
        """
        Asynchronously fetch unique values of given column.
        """
        try:
            data = await self.data_loader_service.fetch_unique_column_values_async(
                table_name=self.table_name,
                column_name=column_name,
            )
            return data
        except Exception as error:
            error_message = f"Failed to get unique values by column '{column_name}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def insert_instruments_config_async(self, raw_data: pd.DataFrame):
        """
        Insert instruments config data into db.
        """
        try:
            await self.data_insertion_service.insert_data(
                raw_data, InstrumentConfigSchema
            )

        except Exception as exc:
            error_message = f"Error inserting data for {self.table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

from typing import List

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import InstrumentConfigError
from src.raw_data.models.config_models import InstrumentConfigModel
from src.raw_data.schemas.config_schemas import InstrumentConfigSchema
from src.raw_data.services.data_insertion_service import GenericDataInsertionService


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

    def get_names_of_columns(self) -> List[str]:
        """
        Get names of columns in instrument config table.
        """
        return [column.name for column in InstrumentConfigModel.__table__.columns]

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
            self.logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument config", error)

    async def get_point_size_of_instrument_async(self, symbol):
        """Asynchronously fetch point size for given instrument."""
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, symbol
            )
            return data[InstrumentConfigSchema.pointsize][0]
        except Exception as error:
            self.logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument config", error)

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
            self.logger.error(
                "Failed to get instrument metadatas asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument metadata", error)

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
            self.logger.error(
                "Failed to get instrument metadatas asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument metadata", error)

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
            self.logger.error(
                "Failed to get instrument metadatas asynchronously: %s",
                error,
                exc_info=True,
            )
            raise InstrumentConfigError("Error fetching instrument metadata", error)

    async def insert_instruments_config_async(self, raw_data: pd.DataFrame):
        """
        Insert instruments config data into db.
        """
        try:
            await self.data_insertion_service.insert_data(
                raw_data, InstrumentConfigSchema
            )

        except Exception as exc:
            self.logger.error(f"Error inserting data for {self.table_name}: {str(exc)}")

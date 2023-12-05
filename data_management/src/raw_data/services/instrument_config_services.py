"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.config_files_errors import InstrumentConfigError
from src.raw_data.models.config_models import InstrumentConfig


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_instrument_configs_async(self):
        """
        Asynchronously fetch instrument config data.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_async(
                InstrumentConfig.__tablename__
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
                InstrumentConfig.__tablename__, symbol
            )
            return data[InstrumentConfig.pointsize.key][0]
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
                InstrumentConfig.__tablename__, symbol
            )
            return data[InstrumentConfig.asset_class.key][0]
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
                table_name=InstrumentConfig.__tablename__,
                column_name=InstrumentConfig.asset_class.key,
                column_value=asset_class,
            )
            return data[InstrumentConfig.symbol.key]
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
                table_name=InstrumentConfig.__tablename__,
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

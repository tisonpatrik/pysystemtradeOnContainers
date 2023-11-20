"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.services.data_load_service import DataLoadService
from src.raw_data.models.config_models import InstrumentConfig
from src.utils.logging import AppLogger


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_files_configs(self):
        """
        Asynchronously instrument config data.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                InstrumentConfig.__tablename__
            )
            return data
        except Exception as error:
            self.logger.error(
                "Failed to get instrumeget_list_of_symbols_asyncnt config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

    async def get_list_of_symbols_async(self):
        """
        Asynchronously fetches list of symbols as a DataFrame.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                InstrumentConfig.__tablename__
            )
            # Use properties from InstrumentConfig to avoid hardcoding
            symbol_column = InstrumentConfig.symbol.key

            # If the data is not empty, return the DataFrame with only the symbol column
            if not data.empty:
                return data[[symbol_column]]
            else:
                self.logger.info("No symbols found in instrument configurations.")
                return pl.DataFrame({symbol_column: []})
        except Exception as error:
            self.logger.error(
                "Failed to get list of symbols asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

    def get_point_size_for_symbol_async(self, symbol: str):
        """
        Asynchronously fetches point size by symbol and return it as a DataFrame using Polars.
        """
        try:
            data = self.get_files_configs_async()
            # Use properties from InstrumentConfig to avoid hardcoding
            symbol_column = InstrumentConfig.symbol.key
            pointsize_column = InstrumentConfig.pointsize.key

            # Filter the DataFrame for the given symbol
            symbol_data = data.filter(pl.col(symbol_column) == symbol)

            # Check if the symbol exists in the data
            if symbol_data.height > 0:
                # Return a DataFrame with only the symbol and pointsize columns
                return symbol_data.select([symbol_column, pointsize_column])
            else:
                self.logger.info(f"No configuration found for symbol: {symbol}")
                # Create an empty DataFrame with the specified columns
                return pl.DataFrame({symbol_column: [], pointsize_column: []})
        except Exception as error:
            self.logger.error(
                "Failed to get point size for symbol asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

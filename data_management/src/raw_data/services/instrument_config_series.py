"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.services.data_load_service import DataLoadService
from src.raw_data.models.config_schemas import InstrumentConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentConfigService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)

    async def get_files_configs_async(self):
        """
        Asynchronously instrument config data.
        """
        try:
            data = await self.data_loader_service.fetch_all_from_table_to_dataframe(
                InstrumentConfig.__tablename__
            )
            return data
        except Exception as error:
            logger.error(
                "Failed to get instrument config asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

    async def get_list_of_symbols_async(self) -> pd.DataFrame:
        """
        Asynchronously fetches list of symbols as a DataFrame.
        """
        try:
            data = await self.get_files_configs_async()
            # Use properties from InstrumentConfig to avoid hardcoding
            symbol_column = InstrumentConfig.symbol.key

            # If the data is not empty, return the DataFrame with only the symbol column
            if not data.empty:
                return data[[symbol_column]]
            else:
                logger.info("No symbols found in instrument configurations.")
                return pd.DataFrame(columns=[symbol_column])
        except Exception as error:
            logger.error(
                "Failed to get list of symbols asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

    async def get_point_size_for_symbol_async(self, symbol: str) -> pd.DataFrame:
        """
        Asynchronously fetches point size by symbol and return it as a DataFrame.
        """
        try:
            data = await self.get_files_configs_async()
            # Use properties from InstrumentConfig to avoid hardcoding
            symbol_column = InstrumentConfig.symbol.key
            pointsize_column = InstrumentConfig.pointsize.key

            # Filter the DataFrame for the given symbol
            symbol_data = data[data[symbol_column] == symbol]

            # Check if the symbol exists in the data
            if not symbol_data.empty:
                # Return a DataFrame with only the symbol and pointsize columns
                return symbol_data[[symbol_column, pointsize_column]]
            else:
                logger.info(f"No configuration found for symbol: {symbol}")
                return pd.DataFrame(columns=[symbol_column, pointsize_column])
        except Exception as error:
            logger.error(
                "Failed to get point size for symbol asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

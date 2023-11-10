"""
This module provides services for fetching and processing instrument config data asynchronously.
"""

import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.services.data_load_service import DataLoadService
from src.core.models.config_schemas import InstrumentConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdjustedPricesService:
    """
    Service for dealing with operations related to instrument config.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)

    async def get_point_size_for_symbol_async(self, symbol: str) -> float:
        """
        Asynchronously fetches point size by symbol and return it as float.
        """
        # try:
        #     data = await self.data_loader_service.fetch_data_from_table_by_symbol(
        #         MultiplePrices.__tablename__, symbol
        #     )
        #     if data.empty:
        #         logger.info(f"No data found for symbol: {symbol}")
        #         return pd.Series()

        #     data = data[[MultiplePrices.unix_date_time.key, MultiplePrices.price.key]]
        #     series = convert_dataframe_to_serie(
        #         data, MultiplePrices.symbol.key, MultiplePrices.unix_date_time.key
        #     )
        #     return series
        # except Exception as error:
        #     logger.error(
        #         "Failed to get denominator prices asynchronously: %s",
        #         error,
        #         exc_info=True,
        #     )
        #     raise

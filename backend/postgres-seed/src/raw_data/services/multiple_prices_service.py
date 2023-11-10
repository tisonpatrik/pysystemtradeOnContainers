"""
This module provides services for fetching and processing multiple prices data asynchronously.
"""

import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    convert_dataframe_to_serie,
)
from src.db.services.data_load_service import DataLoadService
from src.core.models.raw_data_schemas import MultiplePrices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdjustedPricesService:
    """
    Service for dealing with operations related to denominator prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)

    async def get_denominator_prices_async(self, symbol: str) -> pd.Series:
        """
        Asynchronously fetches denominator prices by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_data_from_table_by_symbol(
                MultiplePrices.__tablename__, symbol
            )
            if data.empty:
                logger.info(f"No data found for symbol: {symbol}")
                return pd.Series()

            data = data[[MultiplePrices.unix_date_time.key, MultiplePrices.price.key]]
            series = convert_dataframe_to_serie(
                data, MultiplePrices.symbol.key, MultiplePrices.unix_date_time.key
            )
            return series
        except Exception as error:
            logger.error(
                "Failed to get denominator prices asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

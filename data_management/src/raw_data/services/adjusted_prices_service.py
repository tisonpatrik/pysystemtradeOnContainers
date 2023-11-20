"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    convert_dataframe_to_serie,
)
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.adjusted_prices_errors import DailyPricesFetchError
from src.raw_data.models.raw_data_models import AdjustedPrices
from src.utils.logging import AppLogger


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_prices_async(self, symbol: str) -> pd.Series:
        """
        Asynchronously fetches daily prices by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                AdjustedPrices.__tablename__, symbol
            )
            data = data[[AdjustedPrices.unix_date_time.key, AdjustedPrices.price.key]]
            series = convert_dataframe_to_serie(data, AdjustedPrices.unix_date_time.key)
            return series
        except Exception as error:
            self.logger.error(
                "Failed to get adjusted prices asynchronously for symbol '%s': %s",
                symbol,
                error,
                exc_info=True,
            )
            raise DailyPricesFetchError(symbol, error)

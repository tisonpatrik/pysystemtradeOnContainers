"""
This module provides services for fetching and processing multiple prices data asynchronously.
"""
import polars as pl
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.models.raw_data_models import MultiplePrices


class MultiplePricesService:
    """
    Service for dealing with operations related to multiple prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_denominator_prices_async(self, symbol: str):
        """
        Asynchronously fetches denominator prices by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                MultiplePrices.__tablename__, symbol
            )
            denominator_prices = data.select(
                [MultiplePrices.unix_date_time.key, MultiplePrices.price.key]
            )
            converted_and_sorted = convert_and_sort_by_time(
                denominator_prices, MultiplePrices.unix_date_time.key
            )
            return converted_and_sorted
        except Exception as error:
            self.logger.error(
                "Failed to get denominator prices asynchronously: %s",
                error,
                exc_info=True,
            )
            raise

"""
This module provides services for fetching and processing multiple prices data asynchronously.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pandas.to_series import convert_frame_to_series
from src.core.polars.date_time_convertions import convert_and_sort_by_time
from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.errors.prices_series_errors import DailyPricesFetchError
from src.raw_data.models.raw_data_models import MultiplePrices


class MultiplePricesService:
    """
    Service for dealing with operations related to multiple prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = MultiplePrices.unix_date_time.key
        self.price_column = MultiplePrices.price.key
        self.table_name = MultiplePrices.__tablename__

    async def get_denominator_prices_async(self, symbol: str):
        """
        Asynchronously fetches denominator prices by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol(
                self.table_name, symbol
            )
            converted_and_sorted = convert_and_sort_by_time(data, self.time_column)
            series = convert_frame_to_series(
                converted_and_sorted, self.time_column, self.price_column
            )
            return series
        except Exception as exc:
            self.logger.error(
                "Failed to get denominator prices asynchronously: %s",
                exc,
                exc_info=True,
            )
            raise DailyPricesFetchError(symbol, exc)

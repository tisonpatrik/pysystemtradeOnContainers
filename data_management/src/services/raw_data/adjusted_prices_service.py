"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.converter import convert_frame_to_series

from common.src.database.entity_repository import EntityRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import AdjustedPrices


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = AdjustedPrices.date_time
        self.table_name = AdjustedPrices.__tablename__
        self.price_column = AdjustedPrices.price

        self.repository = EntityRepository(db_session, AdjustedPrices)

    async def get_daily_prices_async(self, symbol: str):
        """
        Asynchronously fetches daily prices by symbol and returns them as Pandas Series.
        """
        try:
            # data = await self.repository.fetch_records_async(self.table_name, symbol)
            # series = convert_frame_to_series(data, self.time_column, self.price_column)
            # return series
            print("neco")
        except Exception as exc:
            error_message = f"Failed to get adjusted prices asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def insert_adjuted_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert adjusted prices data into db.
        """
        try:
            # await self.repository.insert_records_async(raw_data, self.table_name)
            print("neco")

        except Exception as exc:
            error_message = f"Error inserting data for {self.table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

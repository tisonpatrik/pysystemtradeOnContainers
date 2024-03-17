"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import pandas as pd
from pandera.typing import DataFrame, Series
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_frame_to_series
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.schemas.adjusted_prices_schemas import AdjustedPrices, DailyPrices

table_name = AdjustedPricesModel.__name__


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = AdjustedPrices.date_time
        self.price_column = AdjustedPrices.price

        self.repository = Repository(db_session, AdjustedPricesModel)

    async def get_daily_prices_async(self, symbol: str) -> Series[DailyPrices]:
        """
        Asynchronously fetches daily prices by symbol and returns them as Pandas Series.
        """
        try:
            dict = {AdjustedPrices.symbol: symbol}
            columns = [AdjustedPrices.date_time, AdjustedPrices.price]
            data = await self.repository.fetch_filtered_data_to_df_async(dict, columns)
            series = convert_frame_to_series(data, self.time_column, self.price_column)
            validated = Series[DailyPrices](series)
            return validated
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
            error_message = f"Error inserting data for {table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import pandas as pd
from asyncpg import Connection
from asyncpg.prepared_stmt import PreparedStatement
from pandera.typing import Series

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_frame_to_series
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.schemas.adjusted_prices_schemas import (AdjustedPricesSchema,
                                                          DailyPricesSchema)


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, db_session: Connection):
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = AdjustedPricesSchema.date_time
        self.price_column = AdjustedPricesSchema.price
        self.repository = Repository(db_session, AdjustedPricesModel)

    async def get_daily_prices_async(self, statement: PreparedStatement) -> Series[DailyPricesSchema]:
        """
        Asynchronously fetches daily prices by symbol and returns them as Pandas Series.
        """
        try:
            columns = [AdjustedPricesSchema.date_time, AdjustedPricesSchema.price]
            data = await self.repository.fetch_many_async(statement)
            data_frame = pd.DataFrame(data, columns=columns)
            series = convert_frame_to_series(data_frame, self.time_column, self.price_column)
            validated = Series[DailyPricesSchema](series)
            return validated
        except Exception as exc:
            error_message = f"Failed to get adjusted prices asynchronously for'{statement.get_parameters()}': {exc}"
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
            error_message = f"Error inserting data for {AdjustedPricesModel.__name__}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

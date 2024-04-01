"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import pandas as pd
from pandera.typing import Series

from common.src.database.repository import Repository
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_frame_to_series
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.schemas.adjusted_prices_schemas import AdjustedPricesSchema, DailyPricesSchema


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, repository: Repository[AdjustedPricesModel]):
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = AdjustedPricesSchema.date_time
        self.price_column = AdjustedPricesSchema.price
        self.repository = repository

    async def get_daily_prices_async(self, symbol: str) -> Series[DailyPricesSchema]:
        """
        Asynchronously fetches daily prices by symbol and returns them as Pandas Series.
        """
        try:

            query = "SELECT price, date_time FROM adjusted_prices WHERE symbol = $1 ORDER BY date_time"
            statement = Statement(query=query, parameters=symbol)
            records = await self.repository.fetch_many_async(statement)
            data_frame = pd.DataFrame(records)
            series = convert_frame_to_series(data_frame, self.time_column, self.price_column)
            validated = Series[DailyPricesSchema](series)
            return validated
        except Exception as exc:
            error_message = f"Failed to get adjusted prices asynchronously: {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

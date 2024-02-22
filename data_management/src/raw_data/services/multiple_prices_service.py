"""
This module provides services for fetching and processing multiple prices data asynchronously.
"""

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.raw_data_models import MultiplePricesModel
from src.app.schemas.raw_data_schemas import MultiplePricesSchema
from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.pandas.date_time_convertions import convert_and_sort_by_time
from src.db.services.data_load_service import DataLoadService
from src.raw_data.services.data_insertion_service import GenericDataInsertionService

from common.logging.logging import AppLogger


class MultiplePricesService:
    """
    Service for dealing with operations related to multiple prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_loader_service = DataLoadService(db_session)
        self.logger = AppLogger.get_instance().get_logger()
        self.time_column = MultiplePricesModel.unix_date_time.key
        self.price_column = MultiplePricesModel.price.key
        self.table_name = MultiplePricesModel.__tablename__
        self.data_insertion_service = GenericDataInsertionService(
            db_session, self.table_name
        )

    async def get_denominator_prices_async(self, symbol: str):
        """
        Asynchronously fetches denominator prices by symbol and returns them as Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
                self.table_name, symbol
            )
            converted_and_sorted = convert_and_sort_by_time(data, self.time_column)
            series = convert_frame_to_series(
                converted_and_sorted, self.time_column, self.price_column
            )
            return series
        except Exception as error:
            error_message = f"Failed to get denominator denominator for instrument '{symbol}' asynchronously: {error}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

    async def insert_multiple_prices_service_async(self, raw_data: pd.DataFrame):
        """
        Insert multiple prices prices data into db.
        """
        try:
            await self.data_insertion_service.insert_data(
                raw_data, MultiplePricesSchema
            )

        except Exception as exc:
            error_message = f"Error inserting data for {self.table_name}: {str(exc)}"
            self.logger.error(error_message)
            raise ValueError(error_message)

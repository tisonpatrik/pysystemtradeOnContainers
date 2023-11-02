"""
This module provides services for fetching and processing adjusted prices data asynchronously.
"""

import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    convert_dataframe_to_dict_of_series,
)
from src.db.services.data_load_service import DataLoadService
from src.raw_data.schemas.adjusted_prices import AdjustedPrices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdjustedPricesService:
    """
    Service for dealing with operations related to adjusted prices.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the service with a database session.
        """
        self.data_loader_service = DataLoadService(db_session)

    async def get_adjusted_prices_async(self) -> dict[str, pd.Series]:
        """
        Asynchronously fetches all adjusted prices and returns them as a dictionary of Pandas Series.
        """
        try:
            data = await self.data_loader_service.fetch_all_from_table_to_dataframe(
                AdjustedPrices.__tablename__
            )
            series = convert_dataframe_to_dict_of_series(
                data, AdjustedPrices.symbol.key, AdjustedPrices.unix_date_time.key
            )
            return series
        except Exception as error:
            logger.error(
                "Failed to get adjusted prices asynchronously: %s", error, exc_info=True
            )
            raise

"""
This module defines a handler class for inserting robust volatility data into a database.
It makes use of DataLoadService for database operations and DateTimeService for date-time data handling.
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.common_utils.utils.data_aggregation.dataframe_to_series import (
    convert_dataframe_to_dict_of_series,
)
from src.db.services.data_load_service import DataLoadService
from src.risk.schemas.robust_volatility_schema import RobustVolatilitySchema
from src.risk.services.robust_volatility_service import RobustVolatilityService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    Handler class responsible for inserting robust volatility data into the database.
    Utilizes DataLoadService for database-related operations and DateTimeService for date-time data manipulation.
    """

    def __init__(self, db_session: AsyncSession):
        self.data_load_service = DataLoadService(db_session)
        self.risk_schema = RobustVolatilitySchema()
        self.robust_volatility_service = RobustVolatilityService()
        self.source_table = "adjusted_prices"

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table, performs date-time conversion,
        and returns a Pandas Series containing the robust volatility data.
        """
        data_frames = await self.data_load_service.fetch_all_from_table_to_dataframe(
            self.source_table
        )

        series_dict = convert_dataframe_to_dict_of_series(
            data_frames, self.risk_schema.symbol_table, self.risk_schema.datetime_table
        )
        for symbol, serie in series_dict.items():
            risk = self.robust_volatility_service.calculate_volatility_for_instrument(
                serie
            )

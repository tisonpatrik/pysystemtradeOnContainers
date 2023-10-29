"""
This module defines a handler class for inserting robust volatility data into a database.
It makes use of DataLoadService for database operations and DateTimeService for date-time data handling.
"""
import logging

from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.schemas.robust_volatility_schema import RobustVolatilitySchema
from src.risk.services.robust_volatility_service import RobustVolatilityService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    """
    Handler class responsible for inserting robust volatility data into the database.
    Utilizes DataLoadService for database-related operations and DateTimeService for date-time data manipulation.
    """

    def __init__(self, db_session):
        self.db_session = db_session
        self.risk_schema = RobustVolatilitySchema()
        self.robust_volatility_service = RobustVolatilityService()

    async def insert_robust_volatility_async(
        self,
    ):
        """
        Asynchronously fetches data from the specified table, performs date-time conversion,
        and returns a Pandas Series containing the robust volatility data.
        """
        adjusted_service = AdjustedPricesService(self.db_session)
        series_dict = await adjusted_service.get_adjusted_prices_async()
        for symbol, serie in series_dict.items():
            risk = self.robust_volatility_service.calculate_volatility_for_instrument(
                serie
            )

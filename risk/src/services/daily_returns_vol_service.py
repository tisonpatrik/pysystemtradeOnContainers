"""Module for calculating robust volatility for financial instruments."""

from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import (
    add_column_and_populate_it_by_value, rename_columns)
from risk.src.estimators.daily_returns_volatility import \
    DailyReturnsVolEstimator
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.schemas.risk_schemas import (DailyReturnsVol,
                                           DailyReturnsVolatilitySchema)


class DailyReturnsVolService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.price_column = DailyReturnsVolatility.daily_returns_volatility
        self.time_column = DailyReturnsVolatility.date_time
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_repository = Repository(db_session, DailyReturnsVolatility)
        self.estimator = DailyReturnsVolEstimator()

    async def insert_daily_returns_vol_async(self, daily_returns_vols, symbol):
        """
        Calculates and insert daily returns volatility of a given prices.
        """
        try:
            framed = convert_series_to_frame(daily_returns_vols)
            populated = add_column_and_populate_it_by_value(
                framed, DailyReturnsVolatilitySchema.symbol, symbol
            )
            renamed = rename_columns(
                populated,
                [
                    DailyReturnsVolatilitySchema.date_time,
                    DailyReturnsVolatilitySchema.daily_returns_volatility,
                    DailyReturnsVolatilitySchema.symbol,
                ],
            )
            validated = DataFrame[DailyReturnsVolatilitySchema](renamed)
            # await self.risk_repository.insert_data_async(validated)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def calculate_daily_returns_vol_async(self, prices)->Series[DailyReturnsVol]:
        """
        Calculates and inserts daily returns volatility for given prices.
        """
        try:
            daily_returns_vols = self.estimator.process_daily_returns_vol(prices)
            return Series[DailyReturnsVol](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

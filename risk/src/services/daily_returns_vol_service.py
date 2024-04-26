"""Module for calculating robust volatility for financial instruments."""

from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.database.statements.insert_statement import InsertStatement
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from risk.src.schemas.risk_schemas import DailyReturnsVolatilitySchema, Volatility


class DailyReturnsVolService:
    """
    Service for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyReturnsVolEstimator()

    async def insert_daily_returns_vol_async(self, daily_returns_vols: Series[Volatility], symbol: str):
        """
        Insert daily returns volatility of a given prices.
        """
        try:

            framed = convert_series_to_frame(daily_returns_vols)
            populated = add_column_and_populate_it_by_value(framed, DailyReturnsVolatilitySchema.symbol, symbol)
            renamed = rename_columns(
                populated,
                [
                    DailyReturnsVolatilitySchema.date_time,
                    DailyReturnsVolatilitySchema.vol_returns,
                    DailyReturnsVolatilitySchema.symbol,
                ],
            )
            validated = DataFrame[DailyReturnsVolatilitySchema](renamed)
            statement = InsertStatement(table_name="daily_returns_volatility", data=validated)
            await self.repository.insert_dataframe_async(statement)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def calculate_daily_returns_vol(self, prices) -> Series[Volatility]:
        """
        Calculates and inserts daily returns volatility for given prices.
        """
        try:
            daily_returns_vols = self.estimator.process_daily_returns_vol(prices)
            return Series[Volatility](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

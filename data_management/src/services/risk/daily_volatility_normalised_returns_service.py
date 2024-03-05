from src.app.models.risk_models import DailyVolNormalizedReturns
from src.app.schemas.risk_schemas import DailyVolNormalizedReturnsSchema
from src.core.pandas.prapare_db_calculations import prepara_data_to_db
from src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns
from src.utils.converter import convert_frame_to_series
from src.utils.table_operations import sort_by_time

from common.src.logging.logger import AppLogger

table_name = DailyVolNormalizedReturns.__tablename__


class DailyVolatilityNormalisedReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalised_returns = DailyVolNormalisedReturns()
        self.price_column = DailyVolNormalizedReturns.normalized_volatility.key
        self.time_column = DailyVolNormalizedReturns.date_time.key

    async def insert_daily_vol_normalised_returns_for_prices_async(
        self, daily_prices, symbol
    ):
        """Calculates and insert daily volatility of a given prices."""
        try:
            self.logger.info("Starting the daily vol for %s symbol.", symbol)
            daily_returns = (
                self.daily_vol_normalised_returns.get_daily_vol_normalised_returns(
                    daily_prices
                )
            )
            prepared_data = prepara_data_to_db(
                daily_returns, DailyVolNormalizedReturns, symbol
            )
            # await self.repository.insert_data_async(
            #     prepared_data, DailyVolNormalizedReturnsSchema
            # )
            print("neco")
        except Exception as exc:
            error_message = f"Error in calculating cumulative volatility returns for {symbol}: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_vol_normalised_returns_async(self, symbol: str):
        """
        Asynchronously fetches daily returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            # data = await self.data_loader_service.fetch_raw_data_from_table_by_symbol_async(
            #     table_name, symbol
            # )
            # converted_and_sorted = sort_by_time(data, self.time_column)
            # series = convert_frame_to_series(
            #     converted_and_sorted, self.time_column, self.price_column
            # )
            # return series
            print("neco")

        except Exception as exc:
            error_message = f"Failed to get daily returns volatility asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

from src.core.data_types_conversion.to_series import convert_frame_to_series
from src.core.pandas.date_time_convertions import convert_and_sort_by_time
from src.core.pandas.prapare_db_calculations import prepara_data_to_db
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.db.services.data_load_service import DataLoadService
from src.risk.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns
from data_management.src.app.models.risk_models import DailyVolNormalizedReturns


class DailyVolatilityNormalisedReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.data_loader_service = DataLoadService(db_session)
        self.daily_vol_normalised_returns = DailyVolNormalisedReturns()
        self.table_name = DailyVolNormalizedReturns.__tablename__
        self.price_column = DailyVolNormalizedReturns.normalized_volatility.key
        self.time_column = DailyVolNormalizedReturns.unix_date_time.key

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
            await self.data_insert_service.async_insert_dataframe_to_table(
                prepared_data, self.table_name
            )
        except Exception as exc:
            error_message = f"Error in calculating cumulative volatility returns for {symbol}: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_vol_normalised_returns_async(self, symbol: str):
        """
        Asynchronously fetches daily returns volatility by symbol and returns them as Pandas Series.
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

        except Exception as exc:
            error_message = f"Failed to get daily returns volatility asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)

from calendar import c

from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns
from risk.src.models.risk_models import DailyVolNormalizedReturnsModel
from risk.src.schemas.risk_schemas import DailyVolNormalizedReturnsSchema, Volatility


class DailyVolatilityNormalisedReturnsService:
    def __init__(self, repository: Repository[DailyVolNormalizedReturnsModel]):
        self.price_column = DailyVolNormalizedReturnsModel.normalized_volatility
        self.time_column = DailyVolNormalizedReturnsModel.date_time
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyVolNormalisedReturns()

    async def insert_daily_vol_normalised_returns_for_prices_async(self, volatility: Series[Volatility], symbol):
        """Calculates and insert daily volatility of a given prices."""
        try:

            framed = convert_series_to_frame(volatility)
            populated = add_column_and_populate_it_by_value(framed, DailyVolNormalizedReturnsSchema.symbol, symbol)
            renamed = rename_columns(
                populated,
                [
                    DailyVolNormalizedReturnsSchema.date_time,
                    DailyVolNormalizedReturnsSchema.normalized_volatility,
                    DailyVolNormalizedReturnsSchema.symbol,
                ],
            )
            validated = DataFrame[DailyVolNormalizedReturnsSchema](renamed)
            # await self.repository.insert_dataframe_async(validated)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def calculate_daily_vol_normalised_returns_async(self, daily_prices) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_daily_vol_normalised_returns(daily_prices)
            cleaned = daily_returns_vols.dropna()
            return Series[Volatility](cleaned)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

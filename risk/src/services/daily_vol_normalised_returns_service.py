import pandas as pd
from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.daily_vol_normalised_returns import DailyVolNormalisedReturns
from risk.src.models.risk_models import DailyVolNormalizedReturnsModel
from risk.src.schemas.risk_schemas import DailyVolNormalizedReturnsSchema, Volatility


class DailyVolatilityNormalisedReturnsService:
    def __init__(self, repository: Repository[DailyVolNormalizedReturnsModel]):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = DailyVolNormalisedReturns()

    async def insert_daily_vol_normalised_returns_for_prices_async(self, volatility: Series[Volatility], symbol):
        """Insert daily volatility normalized returns of a given prices."""
        try:

            framed = convert_series_to_frame(volatility)
            populated = add_column_and_populate_it_by_value(framed, DailyVolNormalizedReturnsSchema.symbol, symbol)
            renamed = rename_columns(
                populated,
                [
                    DailyVolNormalizedReturnsSchema.date_time,
                    DailyVolNormalizedReturnsSchema.vol_normalized_returns,
                    DailyVolNormalizedReturnsSchema.symbol,
                ],
            )
            validated = DataFrame[DailyVolNormalizedReturnsSchema](renamed)
            await self.repository.insert_dataframe_async(validated)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def calculate_daily_vol_normalised_returns_async(self, daily_prices) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_daily_vol_normalised_returns(daily_prices)
            cleaned = daily_returns_vols.dropna()
            return Series[Volatility](cleaned)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def get_daily_vol_normalised_returns_for_instruments_async(
        self, asset: str
    ) -> DataFrame[DailyVolNormalizedReturnsSchema]:
        """ """
        try:
            query = "SELECT drvm.date_time, drvm.symbol, drvm.vol_normalized_returns FROM daily_vol_normalized_returns AS drvm JOIN instrument_config AS icm ON drvm.symbol = icm.symbol WHERE icm.asset_class = $1;"
            statement = Statement(query=query, parameters=asset)
            record_dicts = await self.repository.fetch_many_async(statement)
            df = pd.DataFrame(record_dicts)
            return DataFrame[DailyVolNormalizedReturnsSchema](df)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

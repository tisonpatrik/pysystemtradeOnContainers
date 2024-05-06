import pandas as pd
from pandera.typing import DataFrame, Series

from common.src.database.statements.insert_statement import InsertStatement
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.instrument_currency_volatility import InstrumentCurrencyVolEstimator
from risk.src.schemas.risk_schemas import InstrumentVolatilitySchema, Volatility


class InstrumentCurrencyVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.estimator = InstrumentCurrencyVolEstimator()

    async def insert_instrument_vol_async(self, volatility: Series[Volatility], symbol: str):
        """
        Insert instrument volatility of a given prices.
        """
        try:

            framed = convert_series_to_frame(volatility)
            populated = add_column_and_populate_it_by_value(framed, InstrumentVolatilitySchema.symbol, symbol)
            renamed = rename_columns(
                populated,
                [
                    InstrumentVolatilitySchema.date_time,
                    InstrumentVolatilitySchema.instrument_volatility,
                    InstrumentVolatilitySchema.symbol,
                ],
            )
            validated = DataFrame[InstrumentVolatilitySchema](renamed)
            statement = InsertStatement(table_name="instrument_currency_volatility", data=validated)
            # await self.repository.insert_dataframe_async(statement)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    def calculate_instrument_vol_async(
        self, denom_price: pd.Series, daily_returns_vol: pd.Series, point_size: float
    ) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_instrument_currency_vol(denom_price, daily_returns_vol, point_size)
            return Series[Volatility](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

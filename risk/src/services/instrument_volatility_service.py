from pandera.typing import DataFrame, Series

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import add_column_and_populate_it_by_value, rename_columns
from risk.src.estimators.instrument_volatility import InstrumentVolEstimator
from risk.src.models.risk_models import InstrumentVolModel
from risk.src.schemas.risk_schemas import InstrumentVolatilitySchema, Volatility


class InstrumentVolService:
    def __init__(self, repository: Repository[InstrumentVolModel]):
        self.price_column = InstrumentVolModel.instrument_volatility
        self.time_column = InstrumentVolModel.date_time
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository
        self.estimator = InstrumentVolEstimator()

    async def insert_instrument_vol_async(self, volatility: Series[Volatility], symbol: str):
        """
        Calculates and insert daily returns volatility of a given prices.
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
            # await self.repository.insert_dataframe_async(validated)

        except Exception as error:
            error_message = f"An error occurred during the processing for symbol '{symbol}': {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def calculate_instrument_vol_async(
        self, multiple_prices, daily_returns_vol, point_size
    ) -> Series[Volatility]:
        """ """
        try:
            daily_returns_vols = self.estimator.get_instrument_currency_vol(
                multiple_prices, daily_returns_vol, point_size
            )
            return Series[Volatility](daily_returns_vols)

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

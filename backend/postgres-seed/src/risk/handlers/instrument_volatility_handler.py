import logging

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from src.db.services.data_insert_service import DataInsertService
from src.core.models.risk_schemas import InstrumentVolatility
from src.raw_data.services.instrument_config_series import InstrumentConfigService
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.risk.services.instrument_volatility import InstrumentVolatilityService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentVolatilityHandler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.instrument_volatility_service = InstrumentVolatilityService()
        self.files_configs_service = InstrumentConfigService(self.db_session)
        self.data_inserter = DataInsertService(self.db_session)
        self.adjusted_service = AdjustedPricesService(self.db_session)
        self.multiple_prices_service = MultiplePricesService(self.db_session)
        self.table_name = InstrumentVolatility.__tablename__

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table,
        performs date-time conversion, and inserts robust volatility data.
        """
        try:
            files_configs = await self.files_configs_service.get_list_of_symbols_async()

            # adjusted_prices = await self.adjusted_service.get_adjusted_prices_async()
            # denominator_prices = (
            #     await self.multiple_prices_service.get_denominator_prices_async()
            # )
            # point_sizes = (
            #     await self.files_configs_service.get_point_size_for_symbol_async()
            # )
            # concatenated_data_frame = await self._process_volatility_data(
            #     denominator_prices, adjusted_prices, point_sizes
            # )

            # await self.data_inserter.async_insert_dataframe_to_table(
            #     concatenated_data_frame, self.table_name
            # )
        except Exception as error:
            logger.error("Failed to insert robust volatility data: %s", error)
            raise

    async def _process_volatility_data(
        self, denominator_prices, adjusted_prices_series, point_sizes
    ):
        """
        Processes volatility data for various financial instruments.
        """
        try:
            processed_data_frames = [
                self.instrument_volatility_service.calculate_instrument_volatility_for_instrument(
                    denominator_prices, adjusted_prices_serie, symbol, point_size
                )
                for symbol, denominator_prices, adjusted_prices_serie, point_size in adjusted_prices_series.items()
            ]

            return concatenate_data_frames(processed_data_frames)
        except Exception as error:
            logger.error("Failed to process volatility data: %s", error)
            raise

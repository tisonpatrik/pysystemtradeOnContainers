import logging

from src.common_utils.utils.data_aggregation.data_aggregators import (
    concatenate_data_frames,
)
from src.db.services.data_insert_service import DataInsertService
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.services.instrument_volatility import InstrumentVolatilityService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustVolatilityHandler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.instrument_volatility_service = InstrumentVolatilityService()
        self.data_inserter = DataInsertService(db_session)
        self.adjusted_service = AdjustedPricesService(self.db_session)
        self.table_name = "robust_volatility"

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table,
        performs date-time conversion, and inserts robust volatility data.
        """
        # try:
        #     adjusted_prices = await self.adjusted_service.get_adjusted_prices_async()
        #     denominator_prices = (
        #         await self.multiple_prices_service.get_denominator_prices_async()
        #     )
        #     point_sizes = await self.config_data_service.get_point_sizes_async()
        #     concatenated_data_frame = await self._process_volatility_data(
        #         denominator_prices, adjusted_prices, point_sizes
        #     )

        #     await self.data_inserter.async_insert_dataframe_to_table(
        #         concatenated_data_frame, self.table_name
        #     )
        # except Exception as error:
        #     logger.error("Failed to insert robust volatility data: %s", error)
        #     raise

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

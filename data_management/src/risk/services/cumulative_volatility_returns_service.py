from src.core.utils.logging import AppLogger
from src.data_seeder.utils.data_aggregators import concatenate_data_frames
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.cumulative_volatility_returns_errors import (
    CumulativeVolatilityReturnsCalculationError,
)
from src.risk.processing.cumulative_volatility_returns import (
    CumulativeVolatilityReturnsCalculator,
)


class CumulativeVolatilityReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.cumulative_volatility_returns_calculator = (
            CumulativeVolatilityReturnsCalculator(db_session)
        )

    async def calculate_cumulative_volatility_returns_for_instrument_async(self, model):
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)
            # Fetch instrument configurations
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs()
            )
            # Process volatilities
            processed_volatilities = await self.cumulative_volatility_returns_calculator.get_cumulative_volatilities_async(
                instrument_configs, model
            )
            # Combine individual volatilities into a single DataFrame
            combined_volatilities = concatenate_data_frames(processed_volatilities)
            return combined_volatilities

        except Exception as exc:
            self.logger.error(
                f"Error in calculating cumulative volatility returns: {exc}"
            )
            raise CumulativeVolatilityReturnsCalculationError()

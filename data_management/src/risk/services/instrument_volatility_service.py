from src.core.utils.logging import AppLogger
from src.data_seeder.utils.data_aggregators import concatenate_data_frames
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.instrument_volatility_errors import (
    InstrumentVolatilityCalculationError,
)
from src.risk.processing.instrument_volatility_processing import (
    InstrumentVolatilityCalculator,
)


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.instrument_volatility_calculator = InstrumentVolatilityCalculator(
            db_session
        )

    async def calculate_instrument_volatility_for_instrument_async(self, model):
        try:
            self.logger.info("Starting the process for %s table.", model.__tablename__)
            # Fetch instrument configurations
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs()
            )

            # Process volatilities
            processed_volatilities = (
                await self.instrument_volatility_calculator.get_volatilities_async(
                    instrument_configs, model
                )
            )
            # Combine individual volatilities into a single DataFrame
            combined_volatilities = concatenate_data_frames(processed_volatilities)
            return combined_volatilities

        except Exception as exc:
            self.logger.error(f"Error in calculating instrument volatility: {exc}")
            raise InstrumentVolatilityCalculationError()

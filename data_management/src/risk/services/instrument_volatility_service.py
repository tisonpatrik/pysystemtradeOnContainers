from src.core.utils.logging import AppLogger
from src.data_seeder.utils.data_aggregators import concatenate_data_frames
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.risk.errors.instrument_volatility_errors import (
    InstrumentVolatilityCalculationError,
)
from src.risk.estimators.instrument_volatility import InstrumentVolEstimator


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.multiple_prices_service = MultiplePricesService(db_session)
        self.instrument_vol_estimator = InstrumentVolEstimator()

    async def insert_instrument_vol_for_prices_async(
        self, multiple_prices, point_size, daily_returns_vol, symbol
    ):
        """Calculates and insert instrument volatility of a given prices."""
        try:
            self.logger.info(
                "Starting the instrument volatility calculation for %s symbol.",
                symbol,
            )

            instrument_volatility = (
                self.instrument_vol_estimator.get_instrument_currency_vol(
                    multiple_prices=multiple_prices,
                    daily_returns_vol=daily_returns_vol,
                    point_size=point_size,
                )
            )
        except Exception as exc:
            self.logger.error(f"Error in calculating instrument volatility: {exc}")
            raise InstrumentVolatilityCalculationError()

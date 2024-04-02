from pandera.errors import SchemaError

from common.src.logging.logger import AppLogger
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from raw_data.src.services.multiple_prices_service import MultiplePricesService
from risk.src.models.risk_models import InstrumentVolModel
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


class SeedInstrumentVolService:
    def __init__(
        self,
        instrument_config_service: InstrumentConfigService,
        daily_returns_vol_service: DailyReturnsVolService,
        multiple_prices_service: MultiplePricesService,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = instrument_config_service
        self.daily_returns_vol_service = daily_returns_vol_service
        self.multiple_prices_service = multiple_prices_service

    async def seed_instrument_volatility_async(self):
        """
        Seed the database with instrument volatility data.
        """
        try:
            self.logger.info(
                "Starting the process for %s table.",
                InstrumentVolModel.__tablename__,
            )
            instruments = await self.instrument_config_service.get_list_of_instruments_async()
            for symbol in instruments:
                multiple_prices = await self.multiple_prices_service.get_denominator_prices_async(symbol.symbol)
                point_size = await self.instrument_config_service.get_point_size_of_instrument_async(symbol.symbol)
                daily_returns_vol = await self.daily_returns_vol_service.calculate_daily_returns_vol_async(
                    multiple_prices
                )
            self.logger.info(
                f"Successfully inserted {InstrumentVolModel.__name__} calculations for {len(instruments)} instruments."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error("An unexpected error occurred during the seeding process: %s", str(e))
            raise

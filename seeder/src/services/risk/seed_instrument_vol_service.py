from pandera.errors import SchemaError

from common.src.logging.logger import AppLogger
from common.src.models.db_models import InstrumentCurrencyVolModel
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from raw_data.src.services.multiple_prices_service import MultiplePricesService
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


class SeedInstrumentVolService:
    def __init__(
        self,
        instrument_config_service: InstrumentConfigService,
        daily_returns_vol_service: DailyReturnsVolService,
        multiple_prices_service: MultiplePricesService,
        instrument_vol_service: InstrumentCurrencyVolService,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = instrument_config_service
        self.daily_returns_vol_service = daily_returns_vol_service
        self.multiple_prices_service = multiple_prices_service
        self.instrument_vol_service = instrument_vol_service

    async def seed_instrument_volatility_async(self):
        """
        Seed the database with instrument volatility data.
        """
        try:
            self.logger.info(
                "Starting the process for %s table.",
                InstrumentCurrencyVolModel.__tablename__,
            )
            instruments = await self.instrument_config_service.get_list_of_instruments_async()
            for symbol in instruments:
                multiple_prices = await self.multiple_prices_service.get_denominator_prices_async(symbol.symbol)
                point_size = await self.instrument_config_service.get_point_size_of_instrument_async(symbol.symbol)
                daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol(multiple_prices)
                instument_vols = self.instrument_vol_service.calculate_instrument_vol_async(
                    multiple_prices, daily_returns_vol, point_size.pointsize
                )
                await self.instrument_vol_service.insert_instrument_vol_async(instument_vols, symbol.symbol)
            self.logger.info(
                f"Successfully inserted {InstrumentCurrencyVolModel.__name__} calculations for {len(instruments)} instruments."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error("An unexpected error occurred during the seeding process: %s", str(e))
            raise

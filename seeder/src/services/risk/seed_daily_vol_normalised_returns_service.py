from pandera.errors import SchemaError

from common.src.logging.logger import AppLogger
from common.src.models.db_models import DailyVolNormalizedReturnsModel
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from risk.src.services.daily_vol_normalised_returns_service import DailyVolatilityNormalisedReturnsService


class SeedDailyVolNormalisedReturnsService:
    """Service for seeding daily volatility normalized returns of financial instruments."""

    def __init__(
        self,
        prices_service: AdjustedPricesService,
        daily_vol_normalised_returns_service: DailyVolatilityNormalisedReturnsService,
        instrument_config_service: InstrumentConfigService,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = instrument_config_service
        self.daily_vol_normalised_returns_service = daily_vol_normalised_returns_service
        self.prices_service = prices_service

    async def seed_daily_normalised_returns_vol_async(self):
        """Seed daily volatility normalised returns."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyVolNormalizedReturnsModel.__tablename__,
            )
            instruments = await self.instrument_config_service.get_list_of_instruments_async()
            for symbol in instruments:
                prices = await self.prices_service.get_daily_prices_async(symbol.symbol)
                daily_vol_normalised_returns = (
                    self.daily_vol_normalised_returns_service.calculate_daily_vol_normalised_returns(prices)
                )
                await self.daily_vol_normalised_returns_service.insert_daily_vol_normalised_returns_for_prices_async(
                    daily_vol_normalised_returns, symbol.symbol
                )
            self.logger.info(
                f"Successfully inserted {DailyVolNormalizedReturnsModel.__name__} calculations for {len(instruments)} instruments."
            )
        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error("An unexpected error occurred during the seeding process: %s", str(e))
            raise

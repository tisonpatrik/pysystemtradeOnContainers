"""Module for calculating robust volatility for financial instruments."""

from pandera.errors import SchemaError

from common.src.database.statement_factory import StatementFactory
from common.src.logging.logger import AppLogger
from raw_data.src.schemas.adjusted_prices_schemas import AdjustedPricesSchema
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(
        self,
        prices_service: AdjustedPricesService,
        daily_returns_vol_service: DailyReturnsVolService,
        instrument_config_service: InstrumentConfigService,
        statement_factory: StatementFactory,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_service = prices_service
        self.daily_returns_vol_service = daily_returns_vol_service
        self.instrument_config_service = instrument_config_service
        self.statement_factory = statement_factory

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )
            instrument_configs = await self.instrument_config_service.get_list_of_instruments_async()

            for config in instrument_configs:
                columns = [AdjustedPricesSchema.date_time, AdjustedPricesSchema.price]
                statement = await self.statement_factory.create_fetch_statement_with_where(
                    columns, f"symbol = '{config.symbol}'"
                )
                prices = await self.prices_service.get_daily_prices_async(statement)
                daily_returns_vol = await self.daily_returns_vol_service.calculate_daily_returns_vol_async(prices)
                await self.daily_returns_vol_service.insert_daily_returns_vol_async(
                    daily_returns_vol, str(config.symbol)
                )
            self.logger.info(
                f"Successfully inserted {DailyReturnsVolatility.__name__} calculations for {len(instrument_configs)} instruments."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error("An unexpected error occurred during the seeding process: %s", str(e))
            raise

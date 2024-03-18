"""Module for calculating robust volatility for financial instruments."""

from pandera.errors import SchemaError

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.services.daily_returns_volatility_service import \
    DailyReturnsVolService


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = Repository(db_session, InstrumentConfig)
        self.prices_repository = Repository(db_session, AdjustedPricesModel)
        self.risk_repository = Repository(db_session, DailyReturnsVolatility)
        self.prices_service = AdjustedPricesService(db_session)
        self.daily_returns_vol_service = DailyReturnsVolService(db_session)

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )

            instrument_configs = await self.instrument_repository.fetch_data_to_df_async()
            for config in instrument_configs.itertuples():
                prices = await self.prices_service.get_daily_prices_async(str(config.symbol))
                daily_returns_vol = self.daily_returns_vol_service.calculate_daily_returns_vol_async(prices)
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
            self.logger.error(
                "An unexpected error occurred during the seeding process: %s", str(e)
            )
            raise

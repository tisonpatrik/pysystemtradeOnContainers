"""Module for calculating robust volatility for financial instruments."""

from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import DailyReturnsVolSeedingError
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.models.risk_models import DailyReturnsVolatility
from src.risk.services.daily_returns_volatility_service import DailyReturnsVolService


class DailyReturnsVolSeedService:
    """Service for calculating daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.adjusted_prices_service = AdjustedPricesService(db_session)
        self.daily_returns_vol_service = DailyReturnsVolService(db_session)

    async def seed_daily_returns_vol_async(self):
        """Calculates daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs_async()
            )
            for config in instrument_configs.to_dict(orient="records"):
                symbol = config[DailyReturnsVolatility.symbol.key]
                daily_prices = (
                    await self.adjusted_prices_service.get_daily_prices_async(symbol)
                )
                await self.daily_returns_vol_service.insert_daily_returns_vol_for_prices_async(
                    daily_prices, symbol
                )
        except DailyReturnsVolSeedingError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise

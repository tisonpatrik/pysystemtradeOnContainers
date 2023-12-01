from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import (
    CumulativeVolatilityReturnsSeedingError,
)
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.models.risk_models import CumulativeDailyVolNormalizedReturns
from src.risk.services.cumulative_volatility_returns_service import (
    CumulativeVolatilityReturnsService,
)


class CumulativeVolSeedService:
    """Service for calculating cumulative volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.adjusted_prices_service = AdjustedPricesService(db_session)
        self.cumulative_volatility_returns_service = CumulativeVolatilityReturnsService(
            db_session
        )

    async def seed_cumulative_volatility_async(self):
        """Calculates cumulative volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                CumulativeDailyVolNormalizedReturns.__tablename__,
            )
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs_async()
            )
            for config in instrument_configs.to_dict(orient="records"):
                symbol = config[CumulativeDailyVolNormalizedReturns.symbol.key]
                daily_prices = (
                    await self.adjusted_prices_service.get_daily_prices_async(symbol)
                )
                await self.cumulative_volatility_returns_service.insert_cumulative_vol_for_prices_async(
                    daily_returns_vol=daily_prices,
                    symbol=symbol,
                )
        except CumulativeVolatilityReturnsSeedingError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise

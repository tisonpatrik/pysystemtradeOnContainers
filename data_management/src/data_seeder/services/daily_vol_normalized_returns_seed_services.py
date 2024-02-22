from src.app.models.risk_models import DailyVolNormalizedReturns
from src.core.utils.logging import AppLogger
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.services.daily_volatility_normalised_returns_service import (
    DailyVolatilityNormalisedReturnsService,
)


class DailyVolNormalisedReturnsSeedService:
    """Service for seeding daily volatility normalized returns of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalised_returns_service = (
            DailyVolatilityNormalisedReturnsService(db_session)
        )
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.adjusted_prices_service = AdjustedPricesService(db_session)

    async def seed_daily_normalised_returns_vol_async(self):
        """Seed daily volatility normalised returns."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyVolNormalizedReturns.__tablename__,
            )
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs_async()
            )
            for config in instrument_configs.to_dict(orient="records"):
                symbol = config[DailyVolNormalizedReturns.symbol.key]
                daily_prices = (
                    await self.adjusted_prices_service.get_daily_prices_async(symbol)
                )
                await self.daily_vol_normalised_returns_service.insert_daily_vol_normalised_returns_for_prices_async(
                    daily_prices, symbol
                )
        except Exception as error:
            error_message = f"An error occurred during seeding: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

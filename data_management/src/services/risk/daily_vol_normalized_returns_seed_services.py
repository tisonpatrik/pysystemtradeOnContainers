from src.services.raw_data.adjusted_prices_service import AdjustedPricesService
from src.services.raw_data.instrument_config_services import \
    InstrumentConfigService
from src.services.risk.daily_volatility_normalised_returns_service import \
    DailyVolatilityNormalisedReturnsService

from common.src.logging.logger import AppLogger
from risk.src.models.risk_models import DailyVolNormalizedReturns


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
            print("neco")
            # for config in instrument_configs:
            #     symbol = config[DailyVolNormalizedReturns.symbol.key]
            #     daily_prices = (
            #         await self.adjusted_prices_service.get_daily_prices_async(symbol)
            #     )
            #     await self.daily_vol_normalised_returns_service.insert_daily_vol_normalised_returns_for_prices_async(
            #         daily_prices, symbol
            #     )
        except Exception as error:
            error_message = f"An error occurred during seeding: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

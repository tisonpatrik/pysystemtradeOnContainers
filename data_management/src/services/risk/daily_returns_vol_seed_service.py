"""Module for calculating robust volatility for financial instruments."""

from src.app.models.risk_models import DailyReturnsVolatility
from src.services.raw_data.adjusted_prices_service import AdjustedPricesService
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.services.risk.daily_returns_volatility_service import DailyReturnsVolService

from common.logging.logger import AppLogger


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.adjusted_prices_service = AdjustedPricesService(db_session)
        self.daily_returns_vol_service = DailyReturnsVolService(db_session)

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
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
        except Exception as error:
            error_message = f"An error occurred during the daily returns volatility seeding process: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

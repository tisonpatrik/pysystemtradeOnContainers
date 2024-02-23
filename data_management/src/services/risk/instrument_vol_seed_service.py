from src.app.models.risk_models import InstrumentVolatility
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.services.raw_data.multiple_prices_service import MultiplePricesService
from src.services.risk.daily_returns_volatility_service import DailyReturnsVolService
from src.services.risk.instrument_volatility_service import InstrumentVolatilityService

from common.logging.logging import AppLogger


class InstrumentVolSeedService:
    """Service for calculating instrument volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.multiple_prices_service = MultiplePricesService(db_session)
        self.instrument_volatility_service = InstrumentVolatilityService(db_session)
        self.daily_returns_vol_service = DailyReturnsVolService(db_session)

    async def seed_instrument_volatility_async(self):
        """Calculates instrument volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                InstrumentVolatility.__tablename__,
            )
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs_async()
            )
            for config in instrument_configs.to_dict(orient="records"):
                symbol = config[InstrumentVolatility.symbol.key]
                multiple_prices = (
                    await self.multiple_prices_service.get_denominator_prices_async(
                        symbol
                    )
                )
                point_size = await self.instrument_config_service.get_point_size_of_instrument_async(
                    symbol
                )

                daily_returns_vol = await self.daily_returns_vol_service.get_daily_returns_volatility_async(
                    symbol
                )
                await self.instrument_volatility_service.insert_instrument_vol_for_prices_async(
                    multiple_prices=multiple_prices,
                    point_size=point_size,
                    daily_returns_vol=daily_returns_vol,
                    symbol=symbol,
                )
        except Exception as error:
            error_message = f"An error occurred during the instrument volatility seeding process: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)

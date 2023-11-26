from src.core.utils.logging import AppLogger
from src.db.services.data_load_service import DataLoadService
from src.raw_data.models.config_models import InstrumentConfig
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.risk.errors.instrument_volatility_errors import (
    InstrumentVolatilityProcessingError,
    VolatilityProcessingHaltedError,
)
from src.risk.estimators.instrument_volatility import get_instrument_currency_vol
from src.risk.services.daily_returns_volatility_service import (
    DailyReturnsVolatilityService,
)


class InstrumentVolatilityCalculator:
    """
    Class for calculating instrument volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_returns_volatility_service = DailyReturnsVolatilityService(
            db_session
        )
        self.data_loader_service = DataLoadService(db_session)
        self.multiple_prices_service = MultiplePricesService(db_session)

    async def get_volatilities_async(self, instrument_configs, model):
        processed_volatilities = []
        for config in instrument_configs.to_dicts():
            try:
                volatility = await self.process_instrument_volatility_async(
                    config, model
                )
                processed_volatilities.append(volatility)
            except InstrumentVolatilityProcessingError as exc:
                self.logger.error(
                    f"Error processing volatility for config {config}: {exc}"
                )
                raise VolatilityProcessingHaltedError()
        return processed_volatilities

    async def process_instrument_volatility_async(self, config, model):
        """
        Process and calculate the volatility for a given instrument configuration.
        """
        try:
            symbol = config[model.symbol.key]
            pointsize = config[InstrumentConfig.pointsize.key]

            # Fetching daily and multiple prices
            daily_returns_vol = await self.daily_returns_volatility_service.get_daily_returns_volatility_async(
                symbol
            )
            multiple_prices = (
                await self.multiple_prices_service.get_denominator_prices_async(symbol)
            )

            # Calculate volatility
            volatility = get_instrument_currency_vol(
                multiple_prices, daily_returns_vol, pointsize
            )
            return volatility

        except KeyError as exc:
            self.logger.error(f"Key error in configuration: {exc}")
            raise InstrumentVolatilityProcessingError()

        except Exception as exc:
            self.logger.error(f"General error processing instrument volatility: {exc}")
            raise InstrumentVolatilityProcessingError()

from src.core.utils.logging import AppLogger
from src.raw_data.models.config_models import InstrumentConfig
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.raw_data.utils.data_aggregators import concatenate_data_frames
from src.risk.errors.instrument_volatility_errors import (
    InstrumentVolatilityCalculationError,
    InstrumentVolatilityProcessingError,
    VolatilityProcessingHaltedError,
)
from src.risk.estimators.instrument_volatility import get_instrument_currency_vol


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_service = AdjustedPricesService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.multiple_prices_service = MultiplePricesService(db_session)

    async def calculate_instrument_volatility_for_instrument_async(self, model):
        try:
            # Fetch instrument configurations
            instrument_configs = (
                await self.instrument_config_service.get_instrument_configs()
            )

            # Process volatilities
            processed_volatilities = await self._get_volatilities_async(
                instrument_configs, model
            )

            # Combine individual volatilities into a single DataFrame
            combined_volatilities = concatenate_data_frames(processed_volatilities)
            return combined_volatilities

        except Exception as exc:
            self.logger.error(f"Error in calculating instrument volatility: {exc}")
            raise InstrumentVolatilityCalculationError()

    async def _get_volatilities_async(self, instrument_configs, model):
        processed_volatilities = []
        for config in instrument_configs.to_dicts():
            try:
                volatility = await self._process_instrument_volatility(config, model)
                processed_volatilities.append(volatility)
            except InstrumentVolatilityProcessingError as exc:
                self.logger.error(
                    f"Error processing volatility for config {config}: {exc}"
                )
                raise VolatilityProcessingHaltedError()
        return processed_volatilities

    async def _process_instrument_volatility(self, config, model):
        """
        Process and calculate the volatility for a given instrument configuration.
        """
        try:
            symbol = config[model.symbol.key]
            pointsize = config[InstrumentConfig.pointsize.key]

            # Fetching daily and multiple prices
            daily_prices = await self.adjusted_prices_service.get_daily_prices_async(
                symbol
            )
            multiple_prices = (
                await self.multiple_prices_service.get_denominator_prices_async(symbol)
            )

            # Calculate volatility
            volatility = get_instrument_currency_vol(
                multiple_prices, daily_prices, pointsize
            )
            return volatility

        except KeyError as exc:
            self.logger.error(f"Key error in configuration: {exc}")
            raise InstrumentVolatilityProcessingError()

        except Exception as exc:
            self.logger.error(f"General error processing instrument volatility: {exc}")
            raise InstrumentVolatilityProcessingError()

from src.core.utils.logging import AppLogger
from src.raw_data.models.config_models import InstrumentConfig
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.risk.estimators.instrument_volatility import get_instrument_currency_vol


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_services = AdjustedPricesService(db_session)
        self.instrument_volatility_services = InstrumentConfigService(db_session)
        self.multiple_prices_services = MultiplePricesService(db_session)

    async def calculate_instrument_volatility_for_instrument_async(self, model):
        instrument_configs = (
            await self.instrument_volatility_services.get_instrument_configs()
        )
        for config in instrument_configs.to_dicts():
            # Assuming the first column in your DataFrame is the symbol
            symbol = config[model.symbol.key]
            poinsize = config[InstrumentConfig.pointsize.key]
            # Pass the symbol to get_daily_prices_async
            daily_prices = await self.adjusted_prices_services.get_daily_prices_async(
                symbol
            )
            multiple_prices = (
                await self.multiple_prices_services.get_denominator_prices_async(symbol)
            )

            volatility = get_instrument_currency_vol(
                multiple_prices, daily_prices, poinsize
            )
        # return data_frame


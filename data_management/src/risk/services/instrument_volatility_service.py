from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.estimators.instrument_volatility import get_instrument_currency_vol
from src.risk.models.risk_models import InstrumentVolatility
from src.utils.logging import AppLogger


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_services = AdjustedPricesService(db_session)
        self.instrument_volatility_service = InstrumentConfigService(db_session)

    async def calculate_instrument_volatility_for_instrument_async(self, model):
        # volatility = get_instrument_currency_vol(
        #     multiple_prices, daily_prices, poinsize
        # )
        # data_frame = process_series_to_frame(
        #     volatility,
        #     symbol,
        #     InstrumentVolatility,
        #     INSTRUMENT_VOLATILITY_COLUMN_MAPPING,
        # )

        instrument_configs = (
            await self.instrument_volatility_service.get_instrument_configs()
        )
        for config in instrument_configs.to_dicts():
            # Assuming the first column in your DataFrame is the symbol
            symbol = config[InstrumentVolatility.symbol.key]
            # Pass the symbol to get_daily_prices_async
            data_frame = await self.adjusted_prices_services.get_daily_prices_async(
                symbol
            )
        # return data_frame

from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.estimators.instrument_volatility import get_instrument_currency_vol
from src.risk.models.risk_models import InstrumentVolatility
from src.utils.logging import AppLogger


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_services = AdjustedPricesService(db_session)

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

        data_frame = await self.adjusted_prices_services.get_daily_prices_async("CORN")
        
        return data_frame

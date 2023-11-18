
from src.db.services.data_load_service import DataLoadService

from src.risk.estimators.instrument_volatility import get_instrument_currency_vol
from src.common_utils.utils.data_to_db.series_to_frame import process_series_to_frame

from src.risk.models.risk_models import InstrumentVolatility
from src.utils.logging import AppLogger

class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_loader = DataLoadService(db_session)

    def calculate_instrument_volatility_for_instrument(self, model):
        try:
            volatility = get_instrument_currency_vol(multiple_prices, daily_prices, poinsize)
            data_frame = process_series_to_frame(volatility,symbol,InstrumentVolatility,INSTRUMENT_VOLATILITY_COLUMN_MAPPING)
            return data_frame
        except Exception as error:
            self.logger.error("Failed to calculate volatility for instrument %s: %s",error, exc_info=True)
            raise

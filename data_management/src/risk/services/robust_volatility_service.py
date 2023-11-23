"""Module for calculating robust volatility for financial instruments."""

from src.core.utils.logging import AppLogger
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.utils.data_aggregators import concatenate_data_frames
from src.risk.errors.robust_vol_processing_error import RobustVolProcessingError
from src.risk.estimators.volatility import robust_vol_calc
from src.risk.models.risk_models import RobustVolatility


class RobustVolatilityService:
    """
    Service for calculating robust volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_series = InstrumentConfigService(db_session)

    async def calculate_robust_volatility_for_instrument_async(self, model):
        """
        Calculates the volatility of a given financial instrument represented by a Pandas Series.
        """
        try:
            i = 0
            # symbols = await self.instrument_config_series.get_list_of_symbols_async()
            # processed_risk_vols = await self._calculate_robust_volatility(
            #     symbols, model
            # )
            # robust_vols = concatenate_data_frames(processed_risk_vols)
            # return robust_vols
        except RobustVolProcessingError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise

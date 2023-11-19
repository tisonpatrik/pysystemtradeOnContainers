"""Module for calculating robust volatility for financial instruments."""

from src.db.services.data_load_service import DataLoadService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.utils.data_aggregators import concatenate_data_frames

from src.risk.estimators.volatility import robust_vol_calc
from src.common_utils.utils.data_to_db.series_to_frame import process_series_to_frame
from src.risk.core.errors.robust_vol_processing_error import RobustVolProcessingError
from src.risk.models.risk_models import RobustVolatility
from src.utils.logging import AppLogger


class RobustVolatilityService:
    """
    Service for calculating robust volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_loader = DataLoadService(db_session)
        self.instrument_config_series = InstrumentConfigService(db_session)

    async def calculate_robust_volatility_for_instrument(self, model):
        """
        Calculates the volatility of a given financial instrument represented by a Pandas Series.
        """
        try:
            symbols = await self.instrument_config_series.get_list_of_symbols_async()
            processed_risk_vols = await self._calculate_robust_volatility(symbols, model)
            robust_vols = concatenate_data_frames(processed_risk_vols)
            return robust_vols
        except RobustVolProcessingError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise

    async def _calculate_robust_volatility(self, symbols, model):
        """
        Processes robust vol for given symbol.
        """
        processed_robust_vol = []
        for symbol in symbols:
            try:
                data_frame = await self.data_loader.fetch_raw_data_from_table_by_symbol(
                    RobustVolatility.__tablename__, symbol
                )
                if data_frame.is_empty():
                    continue

            except Exception as exc:
                self.logger.error(
                    "An unexpected error occurred while processing data for symbol %s: %s",
                    symbol,
                    exc,
                )
                raise RobustVolProcessingError(
                    f"An unexpected error occurred during processing of data for symbol {symbol}."
                ) from exc
        return processed_robust_vol

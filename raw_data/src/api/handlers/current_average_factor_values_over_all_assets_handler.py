import pandas as pd

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.factor_values_all_instruments_handler import FactorValuesAllInstrumentsHandler


class CurrentAverageFactorValuesOverAllAssetsHandler:
    def __init__(
        self,
        factor_values_all_instruments_handler: FactorValuesAllInstrumentsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.factor_values_all_instruments_handler = factor_values_all_instruments_handler

    async def get_current_avg_factor_values_for_all_assets_async(self, factor_name: str, lookback: int) -> pd.Series:
        try:
            all_factor_values = await self.factor_values_all_instruments_handler.get_factor_values_for_all_instruments_async(
                factor_name=factor_name, lookback=lookback
            )
            return all_factor_values.ffill().mean(axis=1)
        except Exception:
            self.logger.exception("Error in processing current average factor values for all assets")
            raise

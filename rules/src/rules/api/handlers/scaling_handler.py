import pandas as pd

from common.src.clients.raw_data_client import RawDataClient
from common.src.logging.logger import AppLogger
from common.src.validation.scaling_type import ScalingType


class ScalingHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client

    async def apply_scaling_to_trading_signal_async(self, symbol: str, raw_forecast: pd.Series, scaling_type: ScalingType) -> pd.Series:
        scaling_methods = {
            ScalingType.none: self._apply_no_scaling,
            ScalingType.fixed: self._apply_fixed_scaling,
            ScalingType.estimated: self._apply_estimated_scaling,
        }
        scaling_function = scaling_methods.get(scaling_type)
        if scaling_function:
            return await scaling_function(symbol, raw_forecast)
        self.logger.exception("Unsupported scaling type: %s", scaling_type)
        raise ValueError("Unsupported scaling type: %s", scaling_type)

    async def _apply_no_scaling(self, symbol: str, raw_forecast: pd.Series) -> pd.Series:
        return raw_forecast  # No scaling applied

    async def _apply_fixed_scaling(self, symbol: str, raw_forecast: pd.Series) -> pd.Series:
        forecast_scalar = 1.5
        return raw_forecast * forecast_scalar

    async def _apply_estimated_scaling(self, symbol: str, raw_forecast: pd.Series) -> pd.Series:
        forecast_scalar = 1.5
        return raw_forecast * forecast_scalar

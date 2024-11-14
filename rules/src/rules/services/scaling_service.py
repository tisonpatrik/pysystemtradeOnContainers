import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.validation.scaling_type import ScalingType


class ScalingService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def apply_scaling_factor_to_signal(self, scaling_factor: float, raw_forecast: pd.Series, scaling_type: ScalingType) -> pd.Series:
        try:
            if scaling_type == ScalingType.NONE:
                return raw_forecast
            if scaling_type == ScalingType.FIXED:
                return raw_forecast * scaling_factor
            raise ValueError(f"Scaling type {scaling_type} is not supported.")

        except Exception as e:
            self.logger.exception("Error occurred in apply_scaling_factor_to_signal_async")
            raise ValueError("Failed to apply scaling factor due to invalid inputs or unexpected data issues.") from e

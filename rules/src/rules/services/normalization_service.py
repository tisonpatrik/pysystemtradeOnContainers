import pandas as pd
from common.validation.scaling_type import ScalingType

from rules.services.capping_service import CappingService
from rules.services.scaling_service import ScalingService


class NormalizationService:
    def __init__(self):
        self.scaling_service = ScalingService()
        self.capping_service = CappingService()

    async def apply_normalization_signal_async(
        self, scaling_factor: float, raw_forecast: pd.Series, scaling_type: str
    ) -> pd.Series:
        scaling_type = ScalingType(scaling_type)
        scaled_signal = self.scaling_service.apply_scaling_factor_to_signal(scaling_factor, raw_forecast, scaling_type)
        return self.capping_service.apply_capping_to_signal(scaled_signal)

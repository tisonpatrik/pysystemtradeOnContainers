import pandas as pd

from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.validation.scaling_type import ScalingType


class ScalingHandler:
    def __init__(self, rules_signals_client: RulesSignalsClient):
        self.rules_signals_client = rules_signals_client

    async def apply_scaling_to_trading_signal_async(
        self, scaling_factor: float, raw_forecast: pd.Series, scaling_type: ScalingType
    ) -> pd.Series:
        if scaling_type.value == ScalingType.none:
            return raw_forecast
        if scaling_type.value == ScalingType.fixed:
            return raw_forecast * scaling_factor
        if scaling_type.value == ScalingType.estimated:
            estimated_scaling_factor = await self.rules_signals_client.get_estimated_scaling_factor_async()
            return raw_forecast * estimated_scaling_factor
        raise ValueError(f"Scaling type {scaling_type} is not supported.")

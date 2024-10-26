import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.relative_momentum import RelativeMomentumService


class RelativeMomentumHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.relative_momentum_service = RelativeMomentumService()

    async def get_relative_momentum_async(self, symbol: str, speed: int) -> pd.Series:
        self.logger.info("Calculating Relative Momentum rule for %s", symbol)
        cumulative_daily_vol_norm_returns = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(symbol)
        normalized_prices_for_asset_class = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
        return self.relative_momentum_service.calculate_relative_momentum(
            cumulative_daily_vol_norm_returns, normalized_prices_for_asset_class, speed
        )

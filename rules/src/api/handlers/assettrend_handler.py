import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.risk_client import RiskClient
from rules.src.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, risk_client: RiskClient, instrument_repository: InstrumentsRepository):
        self.risk_client = risk_client
        self.instrument_repository = instrument_repository
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()

    async def get_assettrend_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating AssetTrend rule for %s by speed %d", symbol, speed)
            asset_class = await self.instrument_repository.get_asset_class_async(symbol)
            prices = await self.risk_client.get_normalized_prices_for_asset_class_async(symbol, asset_class.asset_class)
            return self.assettrend_service.calculate_assettrend(prices, speed)
        except Exception:
            self.logger.exception("Error calculating AssetTrend rule for %s by speed %d", symbol, speed)
            raise

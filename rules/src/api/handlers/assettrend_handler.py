import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.src.services.assettrend import AssettrendService
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.risk_client import RiskClient

class AssettrendHandler:
    def __init__(self, risk_client: RiskClient,instrument_repository: InstrumentsRepository):
        self.raw_data_client = risk_client
        self.instrument_repository=instrument_repository
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()

    async def get_assettrend_async(self, request: GetRuleForInstrumentQuery) -> pd.Series:
        try:
            self.logger.info(f"Calculating AssetTrend rule for {request}")
            asset_class = await self.instrument_repository.get_asset_class_async(request.symbol)
            prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(request.symbol, asset_class.asset_class)
            assettrend = self.assettrend_service.calculate_assettrend(prices, request.speed)
            assettrend = assettrend.dropna()
            return assettrend
        except Exception as e:
            self.logger.error(f"Error calculating AssetTrend rule for {request}: {str(e)}")
            raise e

import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()
        self.raw_data_client = raw_data_client

    async def get_assettrend_async(self, request: GetRuleForInstrumentQuery) -> pd.Series:
        try:
            self.logger.info(f"Calculating AssetTrend rule for {request}")
            daily_prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(request.symbol)
            assettrend = self.assettrend_service.calculate_assettrend(daily_prices, request.speed)
            assettrend = assettrend.dropna()
            return assettrend
        except Exception as e:
            self.logger.error(f"Error calculating AssetTrend rule for {request}: {str(e)}")
            raise e

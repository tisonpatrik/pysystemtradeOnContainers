import pandas as pd

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.assettrend import AssettrendService


class AssettrendHandler:
    def __init__(self, raw_data_client: RawDataClient, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.assettrend_service = AssettrendService()
        self.raw_data_client = raw_data_client
        self.client = client

    async def get_assettrend_async(self, request: GetRuleForInstrumentQuery) -> pd.Series:
        self.logger.info(f"Calculating AssetTrend rule for {request}")
        daily_prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(request.symbol)
        assettrend = self.assettrend_service.calculate_assettrend(daily_prices, request.speed)
        return assettrend

import pandas as pd
from fastapi import HTTPException

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import GetNormalizedPriceForAssetClassQuery
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import dict_to_series
from common.src.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass


class RawDataClient:
    def __init__(self, client: RestClient):
        self.client = client
        self.logger = AppLogger.get_instance().get_logger()

    async def get_normalized_prices_for_asset_class_async(self, instrument_code: str) -> pd.Series:
        query = GetNormalizedPriceForAssetClassQuery(symbol=instrument_code)
        try:
            vol_data = await self.client.get_data_async(query)
            vol = dict_to_series(
                vol_data,
                NormalizedPricesForAssetClass,
                NormalizedPricesForAssetClass.date_time,  # type: ignore[arg-type]
                NormalizedPricesForAssetClass.vol,  # type: ignore[arg-type]
            )
            return vol
        except Exception as e:
            self.logger.error(f"Error fetching daily returns vol rate for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching daily returns vol rate")

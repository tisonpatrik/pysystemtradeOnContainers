import httpx
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
            self.logger.info(f"Received data for {instrument_code}: {vol_data}")  # Log received data
            vol = dict_to_series(
                vol_data,
                NormalizedPricesForAssetClass,
                NormalizedPricesForAssetClass.date_time,  # type: ignore[arg-type]
                NormalizedPricesForAssetClass.vol,  # type: ignore[arg-type]
            )
            return vol

        except httpx.HTTPStatusError as http_exc:
            self.logger.error(
                f"HTTP error occurred while fetching data for {instrument_code}: {http_exc.response.status_code} - {http_exc.response.text}"
            )
            raise HTTPException(status_code=http_exc.response.status_code, detail=f"HTTP error: {http_exc.response.text}")
        except httpx.RequestError as req_exc:
            self.logger.error(f"Request error occurred while fetching data for {instrument_code}: {req_exc}")
            raise HTTPException(status_code=500, detail=f"Request error: {req_exc}")
        except Exception as e:
            self.logger.error(f"Error fetching daily returns vol rate for {instrument_code}: {str(e)}")
            self.logger.debug(e, exc_info=True)  # Log the full stack trace for debugging
            raise HTTPException(status_code=500, detail="Error in fetching daily returns vol rate")

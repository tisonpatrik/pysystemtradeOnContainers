import httpx
import pandas as pd
from fastapi import HTTPException
from pydantic import ValidationError

from common.src.logging.logger import AppLogger
from common.src.models.api_query_models import GetFxRateQuery


class TestHandler:
    def __init__(self, requests_client: httpx.AsyncClient) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.requests_client = requests_client

    async def get_test_fx(self, query: GetFxRateQuery) -> pd.Series:
        try:
            # Serialize query parameters
            query_params = query.model_dump()
            url = "http://raw_data:8000/fx_prices_route/get_fx_rate_by_symbol/"
            response = await self.requests_client.get(url, params=query_params)
            response.raise_for_status()
            json_response = response.json()
            return pd.Series(json_response)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=f"Invalid query parameters: {str(e)}")
        except httpx.RequestError as e:
            self.logger.error(f"Request error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Unable to reach the service, details: {str(e)}")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP status error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

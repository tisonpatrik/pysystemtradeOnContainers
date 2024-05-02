import httpx
import pandas as pd
from fastapi import HTTPException

from common.src.logging.logger import AppLogger


class TestHandler:
    def __init__(self, requests_client: httpx.AsyncClient) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.requests_client = requests_client

    async def get_test_fx(self, symbol: str) -> pd.DataFrame:
        try:
            response = await self.requests_client.get(
                f"http://raw_data:8000/fx_prices_route/get_fx_rate_by_symbol/{symbol}/"
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"Unable to reach the service, details: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch data")

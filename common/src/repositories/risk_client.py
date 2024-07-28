import pandas as pd
from fastapi import HTTPException

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_series
from common.src.validation.daily_returns_vol import DailyReturnsVol


class RiskClient:
    def __init__(self, client: RestClient):
        self.client = client
        self.logger = AppLogger.get_instance().get_logger()

    async def get_daily_retuns_vol_async(self, instrument_code: str) -> pd.Series:
        query = GetDailyReturnsVolQuery(symbol=instrument_code)
        try:
            vol_data = await self.client.get_data_async(query)
            vol = to_series(vol_data, DailyReturnsVol, str(DailyReturnsVol.date_time), str(DailyReturnsVol.vol))
            return vol
        except Exception as e:
            self.logger.error(f"Error fetching daily returns vol rate for {instrument_code}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error in fetching daily returns vol rate")

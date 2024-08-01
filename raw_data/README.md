from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp


class DailyReturnsVol(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)
    vol: Float = Field(coerce=True, nullable=True)
-----import pandas as pd
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
----from typing import Optional, Type, TypeVar, cast

import pandas as pd
from pandera import DataFrameModel
from pydantic import BaseModel

S = TypeVar("S", bound=BaseModel)
T = TypeVar("T", bound=DataFrameModel)


def to_pydantic(item: Optional[dict], model: Type[S]) -> Optional[S]:
    if item is None:
        return None
    else:
        return model(**item)


def to_series(items: list[dict], model: Type[T], index_column: str, values_column: str) -> pd.Series:
    data = pd.DataFrame(items)
    validated_data = model.validate(data)
    data_frame = cast(pd.DataFrame, validated_data)
    series = pd.Series(data_frame[values_column].values, index=data_frame[index_column])
    return series


def to_dataframe(series: pd.Series, model: Type[T], index_column: str, values_column: str) -> pd.DataFrame:
    data = pd.DataFrame({index_column: series.index, values_column: series.values})
    validated_data = model.validate(data)
    data_frame = cast(pd.DataFrame, validated_data)

    return data_frame
-----vytvor novou metodu to_series_from_json kde vstup bude json string ve tvaru
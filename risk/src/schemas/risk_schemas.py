from pandera import DataFrameModel, Field
from pandera.dtypes import Timestamp
from pandera.typing import Index, Series


class CumulativeVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    cum_vol_norm_returns: Series[float] = Field(nullable=True)

    class Config:
        strict = True


class DailyVolNormalizedReturnsSchema(DataFrameModel):
    date_time: Index[Timestamp] = Field(nullable=True)
    vol_normalized_returns: Series[float] = Field(nullable=True)

    class Config:
        strict = True


class Volatility(DataFrameModel):
    date_time: Index[Timestamp] = Field(coerce=True)
    volatility: Series[float]

    class Config:
        strict = True

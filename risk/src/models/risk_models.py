from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseEntity


class DailyReturnsVolatility(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    daily_returns_volatility: float


class InstrumentVolatility(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    instrument_volatility: float


class DailyVolNormalizedReturns(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    normalized_volatility: float


class DailyVolNormalisedPriceForAssetClass(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    asset_clas: str
    normalized_volatility: float

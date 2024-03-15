from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseRecord


class DailyReturnsVolatility(BaseRecord, table=True):
    __name__ = "daily_returns_volatility"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    daily_returns_volatility: float


class InstrumentVolatility(BaseRecord, table=True):
    __name__ = "instrument_volatility"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    instrument_volatility: float


class DailyVolNormalizedReturns(BaseRecord, table=True):
    __name__ = "daily_vol_normalized_returns"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    normalized_volatility: float


class DailyVolNormalisedPriceForAssetClass(BaseRecord, table=True):
    __name__ = "daily_vol_normalised_price_for_asset_class"
    date_time: datetime = Field(primary_key=True)
    asset_clas: str
    normalized_volatility: float

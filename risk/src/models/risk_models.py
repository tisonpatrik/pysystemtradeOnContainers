from datetime import datetime

from sqlmodel import Field

from common.src.db.base_model import BaseModel


class DailyReturnsVolatility(BaseModel, table=True):
    __tablename__ = "daily_returns_volatility"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    daily_returns_volatility: float


class InstrumentVolatility(BaseModel, table=True):
    __tablename__ = "instrument_volatility"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    instrument_volatility: float


class DailyVolNormalizedReturns(BaseModel, table=True):
    __tablename__ = "daily_vol_normalized_returns"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    normalized_volatility: float


class DailyVolNormalisedPriceForAssetClass(BaseModel, table=True):
    __tablename__ = "daily_vol_normalised_price_for_asset_class"
    date_time: datetime = Field(primary_key=True)
    asset_clas: str
    normalized_volatility: float

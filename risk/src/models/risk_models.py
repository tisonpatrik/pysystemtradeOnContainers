from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseModel


class DailyReturnsVolModel(BaseModel, table=True, index=True):
    __tablename__ = "daily_returns_volatility"
    date_time: datetime = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol")
    vol_returns: float


class InstrumentVolModel(BaseModel, table=True):
    __tablename__ = "instrument_volatility"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol")
    instrument_volatility: float


class DailyVolNormalizedReturnsModel(BaseModel, table=True):
    __tablename__ = "daily_vol_normalized_returns"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol")
    vol_normalized_returns: float


class DailyVolNormalisedPriceForAssetClassModel(BaseModel, table=True):
    __tablename__ = "daily_vol_normalised_price_for_asset_class"
    date_time: datetime = Field(primary_key=True)
    asset_clas: str
    vol_normalized_price_for_asset: float

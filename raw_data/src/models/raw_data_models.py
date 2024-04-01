from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseModel


class AdjustedPricesModel(BaseModel, table=True):
    __tablename__ = "adjusted_prices"
    date_time: datetime = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol", index=True)
    price: float


class FxPricesModel(BaseModel, table=True):
    __tablename__ = "fx_prices"
    date_time: datetime = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True, index=True)
    price: float


class MultiplePricesModel(BaseModel, table=True):
    __tablename__ = "multiple_prices"
    date_time: datetime = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol", index=True)
    carry: float = Field(default=None, nullable=True)
    carry_contract: int
    price: float
    price_contract: int
    forward: float = Field(default=None, nullable=True)
    forward_contract: int


class RollCalendarsModel(BaseModel, table=True):
    __tablename__ = "roll_calendars"
    date_time: datetime = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True, foreign_key="instrument_config.symbol", index=True)
    current_contract: int
    next_contract: int
    carry_contract: int

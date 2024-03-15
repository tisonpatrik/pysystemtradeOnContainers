from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseRecord


class AdjustedPrices(BaseRecord, table=True):
    __name__ = "adjusted_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    price: float


class FxPrices(BaseRecord, table=True):
    __name__ = "fx_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str
    price: float


class MultiplePrices(BaseRecord, table=True):
    __name__ = "multiple_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    carry: float
    carry_contract: int
    price: float
    price_contract: int
    forward: float
    forward_contract: int


class RollCalendars(BaseRecord, table=True):
    __name__ = "roll_calendars"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    current_contract: int
    next_contract: int
    carry_contract: int

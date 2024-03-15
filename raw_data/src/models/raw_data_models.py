from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseEntity


class AdjustedPrices(BaseEntity, table=True):

    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    price: float


class FxPrices(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str
    price: float


class MultiplePrices(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    carry: float
    carry_contract: int
    price: float
    price_contract: int
    forward: float
    forward_contract: int


class RollCalendars(BaseEntity, table=True):
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    current_contract: int
    next_contract: int
    carry_contract: int

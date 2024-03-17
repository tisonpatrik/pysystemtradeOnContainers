from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseEntity, BaseRecord


class AdjustedPricesModel(BaseRecord, table=True):
    __tablename__ = "adjusted_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    price: float


class FxPricesModel(BaseRecord, table=True):
    __tablename__ = "fx_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True)
    price: float


class MultiplePricesModel(BaseRecord, table=True):
    __tablename__ = "multiple_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    carry: float = Field(default=None, nullable=True)
    carry_contract: int
    price: float
    price_contract: int
    forward: float = Field(default=None, nullable=True)
    forward_contract: int


class RollCalendarsModel(BaseRecord, table=True):
    __tablename__ = "roll_calendars"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    current_contract: int
    next_contract: int
    carry_contract: int

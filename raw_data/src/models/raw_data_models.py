from datetime import datetime

from sqlmodel import Field

from common.src.database.base_model import BaseRecord


class AdjustedPrices(BaseRecord, table=True):
    __tablename__ = "adjusted_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    price: float


class FxPrices(BaseRecord, table=True):
    __tablename__ = "fx_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str
    price: float


class MultiplePrices(BaseRecord, table=True):
    __tablename__ = "multiple_prices"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    carry: float


class RollCalendars(BaseRecord, table=True):
    __tablename__ = "roll_calendars"
    date_time: datetime = Field(primary_key=True)
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    current_contract: int

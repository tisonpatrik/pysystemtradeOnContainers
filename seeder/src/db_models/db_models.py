from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class InstrumentConfigModel(BaseModel):
    __tablename__ = "instrument_config"
    symbol = Column(String, primary_key=True)
    description = Column(String)
    pointsize = Column(Float)
    currency = Column(String)
    asset_class = Column(String)
    per_block = Column(Float)
    percentage = Column(Float)
    per_trade = Column(Integer)
    region = Column(String)


class InstrumentMetadataModel(BaseModel):
    __tablename__ = "instrument_metadata"
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True)
    asset_class = Column(String)
    sub_class = Column(String)
    description = Column(String)


class RollConfigModel(BaseModel):
    __tablename__ = "roll_config"
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True)
    hold_roll_cycle = Column(String)
    roll_offset_days = Column(Integer)
    carry_offset = Column(Integer)
    priced_roll_cycle = Column(String)
    expiry_offset = Column(Integer)


class SpreadCostsModel(BaseModel):
    __tablename__ = "spred_costs"
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True)
    spread_costs = Column(Float)


class AdjustedPricesModel(BaseModel):
    __tablename__ = "adjusted_prices"
    time = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True, index=True)
    price = Column(Float)
    __table_args__ = (
        Index("ix_adjusted_prices_time", "time"),
        Index("ix_adjusted_prices_symbol", "symbol"),
    )


class FxPricesModel(BaseModel):
    __tablename__ = "fx_prices"
    time = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, primary_key=True, index=True)
    price = Column(Float)
    __table_args__ = (
        Index("ix_fx_prices_time", "time"),
        Index("ix_fx_prices_symbol", "symbol"),
    )


class MultiplePricesModel(BaseModel):
    __tablename__ = "multiple_prices"
    time = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True, index=True)
    carry = Column(Float, nullable=True, default=None)
    carry_contract = Column(Integer)
    price = Column(Float)
    price_contract = Column(Integer)
    forward = Column(Float, nullable=True, default=None)
    forward_contract = Column(Integer)
    __table_args__ = (
        Index("ix_multiple_prices_time", "time"),
        Index("ix_multiple_prices_symbol", "symbol"),
    )


class RollCalendarsModel(BaseModel):
    __tablename__ = "roll_calendars"
    time = Column(DateTime, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("instrument_config.symbol"), primary_key=True, index=True)
    current_contract = Column(Integer)
    next_contract = Column(Integer)
    carry_contract = Column(Integer)
    __table_args__ = (
        Index("ix_roll_calendars_time", "time"),
        Index("ix_roll_calendars_symbol", "symbol"),
    )


class RuleModel(BaseModel):
    __tablename__ = "rules"
    name = Column(String)
    speed = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint("name", "speed"),)

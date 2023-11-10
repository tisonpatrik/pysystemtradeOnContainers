from sqlalchemy import Column, String, Float, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class InstrumentConfig(Base):
    __tablename__ = "instrument_config"

    symbol = Column(String(50), primary_key=True)
    description = Column(Text)
    pointsize = Column(Float)
    currency = Column(String(10))
    asset_class = Column(String(50))
    per_block = Column(Float)
    percentage = Column(Float)
    per_trade = Column(Integer)
    region = Column(String(50))

    def __repr__(self):
        return f"<InstrumentConfig(symbol={self.symbol}, description={self.description}, ...)>"


class InstrumentMetadata(Base):
    __tablename__ = "instrument_metadata"

    symbol = Column(String(50), primary_key=True)
    asset_class = Column(String(50))
    sub_class = Column(String(50))
    sub_sub_class = Column(String(50))
    description = Column(String(100))

    def __repr__(self):
        return f"<InstrumentMetadata(symbol={self.symbol}, asset_class={self.asset_class}, ...)>"


class RollConfig(Base):
    __tablename__ = "roll_config"

    symbol = Column(String(50), primary_key=True)
    hold_roll_cycle = Column(String(50))
    roll_offset_days = Column(Integer)
    carry_offset = Column(Integer)
    priced_roll_cycle = Column(String(50))
    expiry_offset = Column(Integer)

    def __repr__(self):
        return f"<RollConfig(symbol={self.symbol}, hold_roll_cycle={self.hold_roll_cycle}, ...)>"


class SpreadCost(Base):
    __tablename__ = "spread_cost"

    symbol = Column(String(50), primary_key=True)
    spread_cost = Column(Float)

    def __repr__(self):
        return f"<SpreadCost(symbol={self.symbol}, spread_cost={self.spread_cost})>"

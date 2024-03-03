from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text

from common.src.database.base_model import BaseModel


class InstrumentConfigModel(BaseModel):
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


class TradableInstrumentsModel(BaseModel):
    __tablename__ = "tradable_instruments"
    symbol = Column(String(50), primary_key=True)


class InstrumentMetadataModel(BaseModel):
    __tablename__ = "instrument_metadata"
    symbol = Column(
        String(50), ForeignKey("instrument_config.symbol"), primary_key=True
    )
    asset_class = Column(String(50))
    sub_class = Column(String(50))
    sub_sub_class = Column(String(50))
    style = Column(String(50))
    country = Column(String(50))
    duration = Column(String(50))
    description = Column(String(100))


class RollConfigModel(BaseModel):
    __tablename__ = "roll_config"
    symbol = Column(
        String(50), ForeignKey("instrument_config.symbol"), primary_key=True
    )
    hold_roll_cycle = Column(String(50))
    roll_offset_days = Column(Integer)
    carry_offset = Column(Integer)
    priced_roll_cycle = Column(String(50))
    expiry_offset = Column(Integer)


class SpreadCostsModel(BaseModel):
    __tablename__ = "spread_costs"
    symbol = Column(
        String(50), ForeignKey("instrument_config.symbol"), primary_key=True
    )
    spread_costs = Column(Float)

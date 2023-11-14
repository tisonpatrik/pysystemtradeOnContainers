from sqlalchemy import Column, String, Float, Integer, Text
from src.core.models.base_model import BaseModel


class InstrumentConfig(BaseModel):
    __tablename__ = "instrument_config"
    file_name = "instrumentconfig.csv"

    symbol = Column(String(50), primary_key=True)
    description = Column(Text)
    pointsize = Column(Float)
    currency = Column(String(10))
    asset_class = Column(String(50))
    per_block = Column(Float)
    percentage = Column(Float)
    per_trade = Column(Integer)
    region = Column(String(50))

class InstrumentMetadata(BaseModel):
    __tablename__ = "instrument_metadata"
    file_name = "moreinstrumentinfo.csv"

    symbol = Column(String(50), primary_key=True)
    asset_class = Column(String(50))
    sub_class = Column(String(50))
    sub_sub_class = Column(String(50))
    description = Column(String(100))

class RollConfig(BaseModel):
    __tablename__ = "roll_config"
    file_name = "rollconfig.csv"

    symbol = Column(String(50), primary_key=True)
    hold_roll_cycle = Column(String(50))
    roll_offset_days = Column(Integer)
    carry_offset = Column(Integer)
    priced_roll_cycle = Column(String(50))
    expiry_offset = Column(Integer)

class SpreadCost(BaseModel):
    __tablename__ = "spread_cost"
    file_name = "spreadcosts.csv"

    symbol = Column(String(50), primary_key=True)
    spread_cost = Column(Float)


from sqlmodel import Field

from common.src.database.base_model import BaseModel


class InstrumentConfig(BaseModel, table=True):
    symbol: str = Field(primary_key=True)
    description: str
    pointsize: float
    currency: str
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class InstrumentMetadata(BaseModel, table=True):
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    asset_class: str
    sub_class: str
    description: str


class RollConfig(BaseModel, table=True):
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    hold_roll_cycle: str
    roll_offset_days: int
    carry_offset: int
    priced_roll_cycle: str
    expiry_offset: int


class SpreadCosts(BaseModel, table=True):
    symbol: str = Field(primary_key=True, foreign_key="instrumentconfig.symbol")
    spread_costs: float

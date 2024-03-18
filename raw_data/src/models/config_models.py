from sqlmodel import Field

from common.src.db.base_model import BaseEntity


class InstrumentConfig(BaseEntity, table=True):
    __tablename__ = "insturment_config"
    symbol: str = Field(primary_key=True)
    description: str
    pointsize: float
    currency: str
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class InstrumentMetadata(BaseEntity, table=True):
    __tablename__ = "insturment_metadata"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    asset_class: str
    sub_class: str
    description: str


class RollConfig(BaseEntity, table=True):
    __tablename__ = "roll_config"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    hold_roll_cycle: str
    roll_offset_days: int
    carry_offset: int
    priced_roll_cycle: str
    expiry_offset: int


class SpreadCosts(BaseEntity, table=True):
    __tablename__ = "spred_costs"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    spread_costs: float

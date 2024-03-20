from sqlmodel import Field

from common.src.database.base_model import BaseModel


class InstrumentMetadata(BaseModel, table=True):
    __tablename__ = "insturment_metadata"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    asset_class: str
    sub_class: str
    description: str


class RollConfig(BaseModel, table=True):
    __tablename__ = "roll_config"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    hold_roll_cycle: str
    roll_offset_days: int
    carry_offset: int
    priced_roll_cycle: str
    expiry_offset: int


class SpreadCosts(BaseModel, table=True):
    __tablename__ = "spred_costs"
    symbol: str = Field(primary_key=True, foreign_key="insturment_config.symbol")
    spread_costs: float

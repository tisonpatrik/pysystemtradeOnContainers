from typing import Optional

from common.src.validations.base_schema import BaseSchema


class InstrumentConfigSchema(BaseSchema):
    symbol: str
    description: str
    pointsize: float
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class InstrumentMetadataSchema(BaseSchema):
    symbol: str
    asset_class: str
    sub_class: str
    sub_sub_class: Optional[str] = None
    style: Optional[str] = None
    country: Optional[str] = None
    duration: Optional[float] = None
    description: Optional[str] = None


class RollConfigSchema(BaseSchema):
    symbol: str
    hold_roll_cycle: str
    roll_offset_days: int
    carry_offset: int
    priced_roll_cycle: str
    expiry_offset: int


class SpreadCostsSchema(BaseSchema):
    symbol: str
    spread_costs: float

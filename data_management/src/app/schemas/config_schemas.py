import pandera as pa
from pandera import Field

class InstrumentConfigSchema(pa.DataFrameModel):
    symbol: str = Field(nullable=False)
    description: str
    pointsize: float
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class InstrumentMetadataSchema(pa.DataFrameModel):
    symbol: str = Field(nullable=False)
    asset_class: str = Field(nullable=False)
    sub_class: str = Field(nullable=False)
    sub_sub_class: str = Field(nullable=True)
    style: str = Field(nullable=True)
    country: str = Field(nullable=True)
    duration: float = Field(nullable=True)
    description: str = Field(nullable=True)


class RollConfigSchema(pa.DataFrameModel):
    symbol: str = Field(nullable=False)
    hold_roll_cycle: str
    roll_offset_days: int
    carry_offset: int
    priced_roll_cycle: str
    expiry_offset: int


class SpreadCostsSchema(pa.DataFrameModel):
    symbol: str = Field(nullable=False)
    spread_costs: float

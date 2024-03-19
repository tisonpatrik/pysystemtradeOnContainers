import pandera as pa
from pandera.typing import Series


class InstrumentMetadataSchema(pa.DataFrameModel):
    symbol: Series[str]
    asset_class: Series[str]
    sub_class: Series[str]
    description: Series[str]

class RollConfigSchema(pa.DataFrameModel):
    symbol: Series[str]
    hold_roll_cycle: Series[str]
    roll_offset_days: Series[int]
    carry_offset: Series[int]
    priced_roll_cycle: Series[str]
    expiry_offset: Series[int]

class SpreadCostsSchema(pa.DataFrameModel):
    symbol: Series[str]
    spread_costs: Series[float]

class InstrumentConfigSchema(pa.DataFrameModel):
    symbol: Series[str]
    description: Series[str]
    pointsize: Series[float]
    currency: Series[str]
    asset_class: Series[str]
    per_block: Series[float]
    percentage: Series[float]
    per_trade: Series[int]
    region: Series[str]
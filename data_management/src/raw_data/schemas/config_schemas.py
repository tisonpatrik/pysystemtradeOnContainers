import pandera as pa
from pandera import Field
from pandera.typing import Series


class TradableInstrumentsSchema(pa.DataFrameModel):
    symbol: Series[str] = Field(nullable=False)


class InstrumentConfigSchema(pa.DataFrameModel):
    symbol: Series[str] = Field(nullable=False)
    description: Series[str]
    pointsize: Series[float]
    asset_class: Series[str]
    per_block: Series[float]
    percentage: Series[float]
    per_trade: Series[int]
    region: Series[str]


class InstrumentMetadataSchema(pa.DataFrameModel):
    symbol: Series[str] = Field(nullable=False)
    asset_class: Series[str] = Field(nullable=False)
    sub_class: Series[str] = Field(nullable=False)
    sub_sub_class: Series[str] = Field(nullable=True)
    style: Series[str] = Field(nullable=True)
    country: Series[str] = Field(nullable=True)
    duration: Series[float] = Field(nullable=True)
    description: Series[str] = Field(nullable=True)


class RollConfigSchema(pa.DataFrameModel):
    symbol: Series[str] = Field(nullable=False)
    hold_roll_cycle: Series[str]
    roll_offset_days: Series[int]
    carry_offset: Series[int]
    priced_roll_cycle: Series[str]
    expiry_offset: Series[int]


class SpreadCostsSchema(pa.DataFrameModel):
    symbol: Series[str] = Field(nullable=False)
    spread_costs: Series[float]
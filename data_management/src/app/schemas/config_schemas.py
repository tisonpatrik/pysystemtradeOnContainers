import pandera as pa
from pandera import Field
from pandera.typing import DataFrame


class TradableInstrumentsSchema(pa.DataFrameModel):
    symbol: DataFrame[str] = Field(nullable=False)


class InstrumentConfigSchema(pa.DataFrameModel):
    symbol: DataFrame[str] = Field(nullable=False)
    description: DataFrame[str]
    pointsize: DataFrame[float]
    asset_class: DataFrame[str]
    per_block: DataFrame[float]
    percentage: DataFrame[float]
    per_trade: DataFrame[int]
    region: DataFrame[str]


class InstrumentMetadataSchema(pa.DataFrameModel):
    symbol: DataFrame[str] = Field(nullable=False)
    asset_class: DataFrame[str] = Field(nullable=False)
    sub_class: DataFrame[str] = Field(nullable=False)
    sub_sub_class: DataFrame[str] = Field(nullable=True)
    style: DataFrame[str] = Field(nullable=True)
    country: DataFrame[str] = Field(nullable=True)
    duration: DataFrame[float] = Field(nullable=True)
    description: DataFrame[str] = Field(nullable=True)


class RollConfigSchema(pa.DataFrameModel):
    symbol: DataFrame[str] = Field(nullable=False)
    hold_roll_cycle: DataFrame[str]
    roll_offset_days: DataFrame[int]
    carry_offset: DataFrame[int]
    priced_roll_cycle: DataFrame[str]
    expiry_offset: DataFrame[int]


class SpreadCostsSchema(pa.DataFrameModel):
    symbol: DataFrame[str] = Field(nullable=False)
    spread_costs: DataFrame[float]

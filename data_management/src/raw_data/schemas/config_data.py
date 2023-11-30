import polars as pl
from pydantic import BaseModel as PydanticBaseModel


class InstrumentConfigData(PydanticBaseModel):
    symbol: pl.Utf8
    description: pl.Utf8
    pointsize: pl.Float32
    currency: pl.Utf8
    asset_class: pl.Utf8
    per_block: pl.Float32
    percentage: pl.Float32
    per_trade: pl.Int64
    region: pl.Utf8


class InstrumentMetadataData(PydanticBaseModel):
    symbol: pl.Utf8
    asset_class: pl.Utf8
    sub_class: pl.Utf8
    sub_sub_class: pl.Utf8
    description: pl.Utf8


class RollConfigData(PydanticBaseModel):
    symbol: pl.Utf8
    hold_roll_cycle: pl.Utf8
    roll_offset_days: pl.Int64
    carry_offset: pl.Int64
    priced_roll_cycle: pl.Utf8
    expiry_offset: pl.Int64


class SpreadCostData(PydanticBaseModel):
    symbol: pl.Utf8
    spread_cost: pl.Float32

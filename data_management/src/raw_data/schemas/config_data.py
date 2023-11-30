import polars as pl


class InstrumentConfigData:
    symbol: pl.Utf8
    description: pl.Utf8
    pointsize: pl.Float32
    currency: pl.Utf8
    asset_class: pl.Utf8
    per_block: pl.Float32
    percentage: pl.Float32
    per_trade: pl.Int64
    region: pl.Utf8


class InstrumentMetadataData:
    symbol: pl.Utf8
    asset_class: pl.Utf8
    sub_class: pl.Utf8
    sub_sub_class: pl.Utf8
    style: pl.Utf8
    country: pl.Utf8
    duration: pl.Utf8
    description: pl.Utf8


class RollConfigData:
    symbol: pl.Utf8
    hold_roll_cycle: pl.Utf8
    roll_offset_days: pl.Int64
    carry_offset: pl.Int64
    priced_roll_cycle: pl.Utf8
    expiry_offset: pl.Int64


class SpreadCostData:
    symbol: pl.Utf8
    spread_cost: pl.Float32

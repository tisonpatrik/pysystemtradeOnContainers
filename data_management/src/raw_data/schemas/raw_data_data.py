import polars as pl


class AdjustedPricesData:
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    price: pl.Float64


class FxPricesData:
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    price: pl.Float64


class MultiplePricesData:
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    carry: pl.Float64
    carry_contract: pl.Int64
    price: pl.Float64
    price_contract: pl.Int64
    forward: pl.Float64
    forward_contract: pl.Int64


class RollCalendarsData:
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    current_contract: pl.Int64
    next_contract: pl.Int64
    carry_contract: pl.Int64

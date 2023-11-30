import polars as pl
from pydantic import BaseModel as PydanticBaseModel


class AdjustedPricesData(PydanticBaseModel):
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    price: pl.Float32


class FxPricesData(PydanticBaseModel):
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    price: pl.Float32


class MultiplePricesData(PydanticBaseModel):
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    carry: pl.Float32
    carry_contract: pl.Int64
    price: pl.Float32
    price_contract: pl.Int64
    forward: pl.Float32
    forward_contract: pl.Int64


class RollCalendarsData(PydanticBaseModel):
    unix_date_time: pl.Int64
    symbol: pl.Utf8
    current_contract: pl.Int64
    next_contract: pl.Int64
    carry_contract: pl.Int64

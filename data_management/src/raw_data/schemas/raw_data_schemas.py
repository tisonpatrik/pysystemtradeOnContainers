from src.raw_data.schemas.base_schema import BaseSchema
from src.raw_data.schemas.raw_data_data import (
    AdjustedPricesData,
    FxPricesData,
    MultiplePricesData,
    RollCalendarsData,
)


class AdjustedPricesSchema(BaseSchema):
    directory = "/path/in/container/adjusted_prices_csv"
    data: AdjustedPricesData


class FxPricesSchema(BaseSchema):
    directory = "/path/in/container/fx_prices_csv"
    data: FxPricesData


class MultiplePricesSchema(BaseSchema):
    directory = "/path/in/container/multiple_prices_csv"
    data: MultiplePricesData


class RollCalendarsSchema(BaseSchema):
    directory = "/path/in/container/roll_calendars_csv"
    data: RollCalendarsData

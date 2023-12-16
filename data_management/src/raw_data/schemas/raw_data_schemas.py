from src.raw_data.schemas.base_schema import BaseSchema
from src.raw_data.schemas.raw_data_data import (
    AdjustedPricesData,
    FxPricesData,
    MultiplePricesData,
    RollCalendarsData,
)


class AdjustedPricesSchema(BaseSchema):
    tablename = "adjusted_prices"
    directory = "/path/in/container/adjusted_prices_csv"
    data: AdjustedPricesData = AdjustedPricesData()
    ignore_symbols = False

class FxPricesSchema(BaseSchema):
    tablename = "fx_prices"
    directory = "/path/in/container/fx_prices_csv"
    data: FxPricesData = FxPricesData()
    ignore_symbols = True


class MultiplePricesSchema(BaseSchema):
    tablename = "multiple_prices"
    directory = "/path/in/container/multiple_prices_csv"
    data: MultiplePricesData = MultiplePricesData()
    ignore_symbols = False


class RollCalendarsSchema(BaseSchema):
    tablename = "roll_calendars"
    directory = "/path/in/container/roll_calendars_csv"
    data: RollCalendarsData = RollCalendarsData()
    ignore_symbols = False


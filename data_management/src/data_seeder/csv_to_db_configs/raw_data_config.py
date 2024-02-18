class AdjustedPricesConfig:
    tablename = "adjusted_prices"
    directory = "/path/in/container/adjusted_prices"
    ignore_symbols = False


class FxPricesSchemaConfig:
    tablename = "fx_prices"
    directory = "/path/in/container/fx_prices"
    ignore_symbols = True


class MultiplePricesConfig:
    tablename = "multiple_prices"
    directory = "/path/in/container/multiple_prices"
    ignore_symbols = False


class RollCalendarsConfig:
    tablename = "roll_calendars"
    directory = "/path/in/container/roll_calendars"
    ignore_symbols = False

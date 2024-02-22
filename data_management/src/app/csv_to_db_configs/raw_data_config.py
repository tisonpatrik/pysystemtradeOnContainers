class AdjustedPricesConfig:
    tablename: str = "adjusted_prices"
    directory: str = "/path/in/container/adjusted_prices"
    file_name: str = "adjusted_prices.csv"


class FxPricesSchemaConfig:
    tablename: str = "fx_prices"
    directory: str = "/path/in/container/fx_prices"
    file_name: str = "fx_prices.csv"


class MultiplePricesConfig:
    tablename: str = "multiple_prices"
    directory: str = "/path/in/container/multiple_prices"
    file_name: str = "multiple_prices.csv"


class RollCalendarsConfig:
    tablename: str = "roll_calendars"
    directory: str = "/path/in/container/roll_calendars"
    file_name: str = "roll_calendars.csv"

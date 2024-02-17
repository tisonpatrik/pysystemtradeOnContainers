class TradableInstruments:
    tablename = "tradable_instruments"
    file_name: str = "tradable_instruments.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentConfig:
    tablename = "instrument_config"
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentMetadata:
    tablename = "instrument_metadata"
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"


class RollConfig:
    tablename = "roll_config"
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class SpreadCost:
    tablename = "spread_cost"
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"

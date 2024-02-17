class TradableInstrumentsConfig:
    tablename = "tradable_instruments"
    file_name: str = "tradable_instruments.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentConfigConfig:
    tablename = "instrument_config"
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentMetadataConfig:
    tablename = "instrument_metadata"
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"


class RollConfigConfig:
    tablename = "roll_config"
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class SpreadCostConfig:
    tablename = "spread_cost"
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"

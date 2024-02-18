class TradableInstrumentsConfig:
    tablename = "tradable_instruments"
    file_name: str = "tradable_instruments.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentConfigConfig:
    tablename = "instrument_config"
    file_name: str = "instrument_config.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentMetadataConfig:
    tablename = "instrument_metadata"
    file_name: str = "instrument_metadata.csv"
    directory: str = "/path/in/container/csvconfig"


class RollConfigConfig:
    tablename = "roll_config"
    file_name: str = "roll_config.csv"
    directory: str = "/path/in/container/csvconfig"


class SpreadCostConfig:
    tablename = "spread_costs"
    file_name: str = "spread_costs.csv"
    directory: str = "/path/in/container/csvconfig"

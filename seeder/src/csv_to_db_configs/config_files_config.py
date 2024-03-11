from pathlib import Path

# project_root = Path(__file__).resolve().parent.parent.parent.parent
# repos_dir = project_root.parent

# path = repos_dir / "pysystemtrade_preprocessing" / "data" / "csvconfig"
# path = str(path)


class InstrumentConfigConfig:
    tablename: str = "instrument_config"
    file_name: str = "instrument_config.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentMetadataConfig:
    tablename: str = "instrument_metadata"
    file_name: str = "instrument_metadata.csv"
    directory: str = "/path/in/container/csvconfig"


class RollConfigConfig:
    tablename: str = "roll_config"
    file_name: str = "roll_config.csv"
    directory: str = "/path/in/container/csvconfig"


class SpreadCostConfig:
    tablename: str = "spread_costs"
    file_name: str = "spread_costs.csv"
    directory: str = "/path/in/container/csvconfig"

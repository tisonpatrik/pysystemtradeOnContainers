from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent.parent
path = "/home/patrik/repos/pysystemtrade_preprocessing/data/csvconfig"


class InstrumentConfigConfig:
    tablename: str = "instrument_config"
    file_name: str = "instrument_config.csv"
    directory: str = path


class InstrumentMetadataConfig:
    tablename: str = "instrument_metadata"
    file_name: str = "instrument_metadata.csv"
    directory: str = path


class RollConfigConfig:
    tablename: str = "roll_config"
    file_name: str = "roll_config.csv"
    directory: str = path


class SpreadCostConfig:
    tablename: str = "spread_costs"
    file_name: str = "spread_costs.csv"
    directory: str = path

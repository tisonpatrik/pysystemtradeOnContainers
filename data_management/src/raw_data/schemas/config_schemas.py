from src.raw_data.schemas.base_schema import BaseSchema
from src.raw_data.schemas.config_data import (
    InstrumentConfigData,
    InstrumentMetadataData,
    RollConfigData,
    SpreadCostData,
    TradableInstrumentsData
)

class TradableInstruments(BaseSchema):
    tablename = "tradable_instruments"
    file_name: str = "tradable_instruments.csv"
    directory: str = "/path/in/container/csvconfig"
    data: TradableInstrumentsData = TradableInstrumentsData()

class InstrumentConfigSchema(BaseSchema):
    tablename = "instrument_config"
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentConfigData = InstrumentConfigData()


class InstrumentMetadataSchema(BaseSchema):
    tablename = "instrument_metadata"
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentMetadataData = InstrumentMetadataData()


class RollConfigSchema(BaseSchema):
    tablename = "roll_config"
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: RollConfigData = RollConfigData()


class SpreadCostSchema(BaseSchema):
    tablename = "spread_cost"
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"
    data: SpreadCostData = SpreadCostData()

from src.raw_data.schemas.base_schema import BaseSchema
from src.raw_data.schemas.config_data import (
    InstrumentConfigData,
    InstrumentMetadataData,
    RollConfigData,
    SpreadCostData,
)


class InstrumentConfigSchema(BaseSchema):
    tablename = "instrument_config"
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentConfigData


class InstrumentMetadataSchema(BaseSchema):
    tablename = "instrument_metadata"
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentMetadataData


class RollConfigSchema(BaseSchema):
    tablename = "roll_config"
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: RollConfigData


class SpreadCostSchema(BaseSchema):
    tablename = "spread_cost"
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"
    data: SpreadCostData

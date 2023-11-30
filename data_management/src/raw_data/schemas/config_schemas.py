from src.raw_data.schemas.base_schema import BaseSchema
from src.raw_data.schemas.config_data import (
    InstrumentConfigData,
    InstrumentMetadataData,
    RollConfigData,
    SpreadCostData,
)


class InstrumentConfigSchema(BaseSchema):
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentConfigData


class InstrumentMetadataSchema(BaseSchema):
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"
    data: InstrumentMetadataData


class RollConfigSchema(BaseSchema):
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"
    data: RollConfigData


class SpreadCostSchema(BaseSchema):
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"
    data: SpreadCostData

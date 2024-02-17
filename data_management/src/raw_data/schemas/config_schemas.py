from src.raw_data.schemas.base_schema import BaseSchema


class TradableInstrumentsSchema(BaseSchema):
    tablename = "tradable_instruments"
    file_name: str = "tradable_instruments.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentConfigSchema(BaseSchema):
    tablename = "instrument_config"
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class InstrumentMetadataSchema(BaseSchema):
    tablename = "instrument_metadata"
    file_name: str = "moreinstrumentinfo.csv"
    directory: str = "/path/in/container/csvconfig"


class RollConfigSchema(BaseSchema):
    tablename = "roll_config"
    file_name: str = "rollconfig.csv"
    directory: str = "/path/in/container/csvconfig"


class SpreadCostSchema(BaseSchema):
    tablename = "spread_cost"
    file_name: str = "spreadcosts.csv"
    directory: str = "/path/in/container/csvconfig"

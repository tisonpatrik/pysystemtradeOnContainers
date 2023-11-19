from pydantic import BaseModel

class InstrumentConfig(BaseModel):
    file_name: str = "instrumentconfig.csv"
    directory: str = "/path/in/container/csvconfig"

class InstrumentMetadata(BaseModel):
    file_name = "moreinstrumentinfo.csv"
    directory = "/path/in/container/csvconfig"

class RollConfig(BaseModel):
    file_name = "rollconfig.csv"
    directory = "/path/in/container/csvconfig"

class SpreadCost(BaseModel):
    file_name = "spreadcosts.csv"
    directory = "/path/in/container/csvconfig"

from pydantic import BaseModel
from pandas import DataFrame

class CsvOutput(BaseModel):
    full_path: str
    dataframe: DataFrame

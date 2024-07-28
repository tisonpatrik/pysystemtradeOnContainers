from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp


class InstrumnentVolatility(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)
    vol: Float = Field(coerce=True, nullable=True)
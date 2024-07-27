from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp


class TradingSignal(DataFrameModel):
    date_time: Timestamp = Field(coerce=True)
    value: Float = Field(coerce=True, nullable=True)

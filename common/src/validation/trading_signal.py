from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp


class TradingSignal(DataFrameModel):
    time: Timestamp = Field(coerce=True) # type: ignore[assignment]
    value: Float = Field(coerce=True, nullable=True)

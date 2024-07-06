from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp


class FxPrices(DataFrameModel):
	date_time: Timestamp = Field(coerce=True)
	price: Float = Field(coerce=True, nullable=True)
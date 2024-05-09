from pandera import DataFrameModel, Field
from pandera.dtypes import Float, Timestamp
from pandera.typing import Series


class DenomPrices(DataFrameModel):
	date_time: Series[Timestamp] = Field(coerce=True)
	price: Series[Float] = Field(coerce=True)

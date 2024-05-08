from pandera import DataFrameModel
from pandera.dtypes import Timestamp
from pandera.typing import Series


class FxPrices(DataFrameModel):
	date_time: Series[Timestamp]
	price: Series[float]

	class Config:
		strict = True
		coerce = True

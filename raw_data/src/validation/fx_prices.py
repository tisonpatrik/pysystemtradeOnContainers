from datetime import datetime

from pandera import DataFrameModel
from pandera.typing import Series


class FxPrices(DataFrameModel):
	date_time: Series[datetime]
	price: Series[float]

	class Config:
		strict = True
		coerce = True

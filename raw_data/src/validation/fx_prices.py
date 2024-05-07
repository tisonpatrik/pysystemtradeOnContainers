from datetime import datetime

import pandera as pa
from pandera.typing import Index, Series


class FxPrices(pa.DataFrameModel):
	date_time: Index[datetime]
	price: Series[float]

	class Config:
		strict = True
		coerce = True

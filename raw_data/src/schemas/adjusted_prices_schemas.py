
from datetime import datetime

import pandera as pa
from pandera.typing import Series


class AdjustedPricesSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    symbol: Series[str]
    price: Series[float]

class DailyPricesSchema(pa.DataFrameModel):
    date_time: Series[datetime]
    price: Series[float]

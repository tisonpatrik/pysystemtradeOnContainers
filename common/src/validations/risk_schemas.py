from datetime import datetime

import pandera as pa
from pandera.typing import Series


class DailyReturns(pa.SeriesSchema):
    date_time: Series[datetime]
    price: Series[float]


class DailyReturnsVolatility(pa.SeriesSchema):
    date_time: Series[datetime]
    price: Series[float]

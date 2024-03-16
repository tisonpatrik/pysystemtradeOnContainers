from datetime import datetime

import pandera as pa
from pandera.typing import Series


class DailyPrices(pa.DataFrameModel):
    date_time: Series[datetime]
    price: Series[float]

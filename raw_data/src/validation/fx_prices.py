from datetime import datetime

import pandera as pa
from pandera.typing import Series


class FxPrices(pa.DataFrameModel):
    date_time: Series[datetime]
    price: Series[float]

    class Config:
        strict = True
        coerce = True

from datetime import datetime

import pandera as pa
from pandera.typing import Series


class BaseSchema(pa.DataFrameModel):
    date_time: Series[datetime]
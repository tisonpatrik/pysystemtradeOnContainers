from datetime import datetime

import pandera as pa
from pandera.typing import Series


class BaseSchema(pa.DataFrameModel):
    date_time: Series[datetime]

    @classmethod
    def get_columns(cls) -> list[str]:
        return list(cls.__annotations__.keys())
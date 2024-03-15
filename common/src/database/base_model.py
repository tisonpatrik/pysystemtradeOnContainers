# base_model.py
from datetime import datetime

import pandera as pa
from pandera.typing import Series
from sqlmodel import SQLModel


class BaseEntity(SQLModel):
    __abstract__ = True


class BaseRecord(pa.DataFrameModel):
    __abstract__ = True
    date_time: Series[datetime]

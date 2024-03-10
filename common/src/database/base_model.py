# base_model.py
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    __abstract__ = True

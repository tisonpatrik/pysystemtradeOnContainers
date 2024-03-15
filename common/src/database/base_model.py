from sqlmodel import SQLModel


class BaseEntity(SQLModel):
    __abstract__ = True


class BaseRecord(SQLModel):
    __abstract__ = True

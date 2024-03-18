from sqlmodel import SQLModel


class BaseEntity(SQLModel):
    __abstract__ = True
    __tablename__: str


class BaseRecord(SQLModel):
    __abstract__ = True
    __tablename__: str

from sqlmodel import SQLModel


class BaseModel(SQLModel):
    __abstract__ = True
    __tablename__: str
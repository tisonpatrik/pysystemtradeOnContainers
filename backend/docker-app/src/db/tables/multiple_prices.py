from sqlmodel import Field, SQLModel

from src.db.tables.base_class import StatusEnum, TimestampModel, UUIDModel


class MultiplePricesBase(SQLModel):
    amount: int = Field(nullable=False)
    description: str = Field(nullable=False)


class MultiplePrices(MultiplePricesBase, UUIDModel, TimestampModel, table=True):
    status: StatusEnum = Field(default=StatusEnum.inactive)

    __tablename__ = "multiple_prices"

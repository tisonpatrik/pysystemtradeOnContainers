from sqlmodel import Field, SQLModel

from src.db.tables.base_class import StatusEnum, TimestampModel, UUIDModel
from src.db.tables.base_class import StatusEnum
from shared.src.entities.multiple_prices import MultiplePrices as BaseMultiplePrices

class MultiplePricesTableBase(SQLModel, BaseMultiplePrices):
    status: StatusEnum = Field(default=StatusEnum.inactive)

# Define the database table model with composite primary key
class MultiplePricesTable(MultiplePricesTableBase, UUIDModel, TimestampModel, table=True):
    UNIX_TIMESTAMP: int = Field(primary_key=True)
    SYMBOL: str = Field(primary_key=True)
    __tablename__ = "multiple_prices"

    def __init__(self, **data):
        super().__init__(**data)


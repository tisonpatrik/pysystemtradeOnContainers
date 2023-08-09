from sqlmodel import Field, SQLModel
from datetime import datetime

# Define the base model
class AdjustedPricesTableBase(SQLModel):
    DATETIME: datetime = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    PRICE: float = Field(nullable=True)

# Define the table model
class AdjustedPricesTable(AdjustedPricesTableBase, table=True):
    __tablename__ = "adjusted_prices"

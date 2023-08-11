from sqlmodel import Field, SQLModel
from datetime import datetime

# Define the base model
class MultiplePricesTableBase(SQLModel):
    DATETIME: datetime = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    CARRY: float = Field(nullable=True)
    CARRY_CONTRACT: int = Field(nullable=True)
    PRICE: float = Field(nullable=True)
    PRICE_CONTRACT: int = Field(nullable=True)
    FORWARD: float = Field(nullable=True)
    FORWARD_CONTRACT: int = Field(nullable=True)
    ADJUSTED_PRICES: float= Field(nullable=True)

# Define the table model
class MultiplePricesTable(MultiplePricesTableBase, table=True):
    __tablename__ = "multiple_prices"
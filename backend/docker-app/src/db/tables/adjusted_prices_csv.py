from sqlmodel import Field, SQLModel

# Define the base model
class AdjustedPricesBase(SQLModel):
    UNIX_TIMESTAMP: int = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    PRICE: float = Field(nullable=True)

# Define the table model
class AdjustedPrices(AdjustedPricesBase, table=True):
    __tablename__ = "adjusted_prices"

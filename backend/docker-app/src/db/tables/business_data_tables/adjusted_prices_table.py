from sqlmodel import Field, SQLModel

# Define the base model
class AdjustedPricesTableBase(SQLModel):
    UNIX_TIMESTAMP: int = Field(primary_key=True, index=True, foreign_key="multiple_prices.SYMBOL")
    SYMBOL: str = Field(primary_key=True, index=True, foreign_key="instrument_config.SYMBOL")
    PRICE: float = Field(nullable=True)

# Define the table model
class AdjustedPricesTable(AdjustedPricesTableBase, table=True):
    __tablename__ = "adjusted_prices"

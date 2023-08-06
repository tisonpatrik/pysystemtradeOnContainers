from sqlmodel import Field, SQLModel

# Define the base model
class FxPricesTableBase(SQLModel):
    UNIX_TIMESTAMP: int = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    PRICE: float = Field(nullable=True)

# Define the table model
class FxPricesTable(FxPricesTableBase, table=True):
    __tablename__ = "fx_prices"
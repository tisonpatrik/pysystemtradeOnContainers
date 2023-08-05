from sqlmodel import Field, SQLModel

# Define the base model
class MultiplePricesBase(SQLModel):
    UNIX_TIMESTAMP: int = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    CARRY: float = Field(nullable=True)
    CARRY_CONTRACT: int = Field(nullable=True)
    PRICE: float = Field(nullable=True)
    PRICE_CONTRACT: int = Field(nullable=True)
    FORWARD: float = Field(nullable=True)
    FORWARD_CONTRACT: int = Field(nullable=True)

# Define the table model
class MultiplePrices(MultiplePricesBase, table=True):
    __tablename__ = "multiple_prices"

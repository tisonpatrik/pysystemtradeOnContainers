from sqlmodel import Field, SQLModel

# Define the base model
class SpreadCostTableBase(SQLModel):
    SYMBOL: str = Field(primary_key=True, index=True, foreign_key="instrument_config.SYMBOL")
    SPREAD_COST: float = Field(nullable=True)

# Define the table model
class SpreadCostTable(SpreadCostTableBase, table=True):
    __tablename__ = "spread_cost"
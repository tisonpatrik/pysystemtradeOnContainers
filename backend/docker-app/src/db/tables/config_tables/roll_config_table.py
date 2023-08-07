from sqlmodel import Field, SQLModel

# Define the base model
class RollConfigTableBase(SQLModel):
    SYMBOL: str = Field(primary_key=True, index=True)
    HOLD_ROLL_CYCLE: str = Field(nullable=True)
    ROLL_OFFSET_DAYS: int = Field(nullable=True)
    CARRY_OFFSET: int = Field(nullable=True)
    PRICED_ROLL_CYCLE: str = Field(nullable=True)
    EXPIRY_OFFSET: int = Field(nullable=True)

# Define the table model
class RollConfigTable(RollConfigTableBase, table=True):
    __tablename__ = "roll_config"
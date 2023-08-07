from sqlmodel import Field, SQLModel

# Define the base model
class RollCalendarsTableBase(SQLModel):
    UNIX_TIMESTAMP: int = Field(primary_key=True, index=True)
    SYMBOL: str = Field(primary_key=True, index=True)
    CURRENT_CONTRACT: int = Field(nullable=True)
    NEXT_CONTRACT: int = Field(nullable=True)
    CARRY_CONTRACT: int = Field(nullable=True)

# Define the table model
class RollCalendarsTable(RollCalendarsTableBase, table=True):
    __tablename__ = "roll_calendars"
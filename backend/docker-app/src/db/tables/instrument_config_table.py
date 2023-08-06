from sqlmodel import Field, SQLModel

# Define the base model
class InstrumentConfigTableBase(SQLModel):
    SYMBOL: str = Field(primary_key=True, index=True)
    DESCRIPTION: str = Field(nullable=True)
    POINTSIZE: float = Field(nullable=True)
    CURRENCY: str = Field(nullable=True)
    ASSET_CLASS: str= Field(nullable=True)
    PER_BLOCK: float = Field(nullable=True)
    PERCENTAGE: float = Field(nullable=True)
    PER_TRADE: float = Field(nullable=True)
    REGION: str = Field(nullable=True)


# Define the table model
class InstrumentConfigTable(InstrumentConfigTableBase, table=True):
    __tablename__ = "instrument_config"
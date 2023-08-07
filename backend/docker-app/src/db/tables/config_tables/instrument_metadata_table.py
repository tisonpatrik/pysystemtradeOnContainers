from sqlmodel import Field, SQLModel

# Define the base model
class InstrumentMetadataTableBase(SQLModel):
    SYMBOL: str = Field(primary_key=True, index=True, foreign_key="instrument_config.SYMBOL")
    ASSET_CLASS: str = Field(nullable=True)
    SUB_CLASS: str = Field(nullable=True)
    SUB_SUB_CLASS: str = Field(nullable=True)
    STYLE: str = Field(nullable=True)
    COUNTRY: str = Field(nullable=True)
    DURATION: str = Field(nullable=True)
    DESCRIPTION: str = Field(nullable=True)

# Define the table model
class InstrumentMetadataTable(InstrumentMetadataTableBase, table=True):
    __tablename__ = "instrument_metadata"

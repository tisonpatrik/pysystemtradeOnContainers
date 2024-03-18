from sqlmodel import Field

from common.src.db.base_model import BaseModel


class InstrumentConfig(BaseModel, table=True):
    __tablename__ = "insturment_config"
    symbol: str = Field(primary_key=True)
    description: str
    pointsize: float
    currency: str
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class Instrument(BaseModel):
    symbol: str

import decimal

from pydantic import BaseModel as Model
from sqlmodel import Field

from common.src.database.base_model import BaseModel


class InstrumentConfigModel(BaseModel, table=True):
    __tablename__ = "instrument_config"
    symbol: str = Field(primary_key=True)
    description: str
    pointsize: float
    currency: str
    asset_class: str
    per_block: float
    percentage: float
    per_trade: int
    region: str


class Instrument(Model):
    symbol: str


class PointSize(Model):
    pointsize: float

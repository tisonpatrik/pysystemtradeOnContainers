from pydantic import BaseModel as Model


class Instrument(Model):
    symbol: str


class AssetClass(Model):
    asset_class: str


class PointSize(Model):
    pointsize: float

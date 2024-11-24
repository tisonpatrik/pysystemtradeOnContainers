from pydantic import BaseModel


class AssetClass(BaseModel):
    asset_class: str

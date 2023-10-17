from pydantic import BaseModel


class AdjustedPricesSchema(BaseModel):
    unix_date_time: int
    symbol: str
    price: float

    class Config:
        orm_mode = True

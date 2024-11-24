from pydantic import BaseModel


class Instrument(BaseModel):
    symbol: str

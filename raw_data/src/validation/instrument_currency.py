from pydantic import BaseModel


class InstrumentCurrency(BaseModel):
    currency: str

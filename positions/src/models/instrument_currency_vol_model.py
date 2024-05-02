from datetime import datetime

from pydantic import BaseModel


class InstrumentCurrencyVolModel(BaseModel):
    date_time: datetime
    instrument_volatility: float

from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class AvaragePositionQuery(BaseModel):
    symbol: Annotated[str, StringConstraints(max_length=10)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]
    annual_cash_vol_target: float

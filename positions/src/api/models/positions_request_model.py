from pydantic import BaseModel, PositiveFloat, StringConstraints
from typing_extensions import Annotated


class SubsystemPositionRequest(BaseModel):
    notional_capital: PositiveFloat
    percentage_volatility_target: PositiveFloat
    avarage_absolute_forecas: PositiveFloat
    instrument: Annotated[str, StringConstraints(max_length=50)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]

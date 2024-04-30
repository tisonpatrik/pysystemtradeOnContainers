from pydantic import BaseModel, PositiveFloat, StringConstraints
from typing_extensions import Annotated


class SimulationRequest(BaseModel):
    notional_capital: PositiveFloat
    target_risk: PositiveFloat
    base_currency: Annotated[str, StringConstraints(max_length=3)]

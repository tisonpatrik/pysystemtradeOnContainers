from typing import Annotated

from pydantic import BaseModel, PositiveFloat, StringConstraints


class RuleRequest(BaseModel):
    symbol: Annotated[str, StringConstraints(max_length=30)]
    use_attenuation: bool
    scaling_type: Annotated[str, StringConstraints(max_length=30)]
    scaling_factor: PositiveFloat

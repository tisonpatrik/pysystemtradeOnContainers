from typing import Annotated

from pydantic import BaseModel, PositiveFloat, StringConstraints


class BaseRuleRequest(BaseModel):
    symbol: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    use_attenuation: bool
    scaling_type: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    scaling_factor: PositiveFloat

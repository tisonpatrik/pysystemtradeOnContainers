from typing import Annotated, Any

from pydantic import BaseModel, Json, StringConstraints


class Rule(BaseModel):
    rule_variation_name: Annotated[str, StringConstraints(max_length=30)]
    rule_name: Annotated[str, StringConstraints(max_length=30)]
    rule_parameters: Json[dict[str, Any]]
    scaling_factor: float
    use_attenuation: bool

from pydantic import BaseModel, NonNegativeInt, StringConstraints
from typing_extensions import Annotated


class Rule(BaseModel):
	name: Annotated[str, StringConstraints(max_length=15)]
	speed: NonNegativeInt

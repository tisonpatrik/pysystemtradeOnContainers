from typing import Annotated

from pydantic import BaseModel, NonNegativeInt, StringConstraints


class Rule(BaseModel):
    name: Annotated[str, StringConstraints(max_length=15)]
    speed: NonNegativeInt

    @property
    def task(self) -> str:
        return f"rules.{self.name}"

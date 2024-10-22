from typing import Literal

from pydantic import BaseModel


class FactorName(BaseModel):
    name: Literal["skew", "neg_skew"]

    @classmethod
    def create(cls, name: Literal["skew", "neg_skew"]):
        return cls(name=name)

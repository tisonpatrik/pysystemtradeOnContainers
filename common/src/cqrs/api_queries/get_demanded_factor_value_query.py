from typing import Literal

from pydantic import BaseModel


class GetDemandedFactorValueQuery(BaseModel):
    symbol: str
    factor_name: Literal["skew", "neg_skew"]
    lookback: int

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/demanded_factor_value_route/get_demanded_factor_value/"

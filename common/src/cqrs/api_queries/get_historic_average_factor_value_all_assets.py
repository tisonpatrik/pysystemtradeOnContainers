from typing import Literal

from pydantic import BaseModel


class GetHistoricAverageFactorValueAllAssetsQuery(BaseModel):
    factor_name: Literal["skew", "neg_skew"]
    lookback: int

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/historic_average_factor_value_all_assets_route/get_historic_average_factor_value_all_assets/"

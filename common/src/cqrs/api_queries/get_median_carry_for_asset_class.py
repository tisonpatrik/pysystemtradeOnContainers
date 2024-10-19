from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetMedianCarryForAssetClassQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/median_carry_for_asset_class_route/get_median_carry_for_asset_class/"

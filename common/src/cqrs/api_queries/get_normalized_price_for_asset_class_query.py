from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetNormalizedPriceForAssetClassQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=15)]
    asset_class: Annotated[str, StringConstraints(max_length=15)]

    @property
    def url_string(self) -> str:
        return "http://risk:8000/normalized_prices_for_asset_class_router/get_normalized_prices_for_asset_class/"

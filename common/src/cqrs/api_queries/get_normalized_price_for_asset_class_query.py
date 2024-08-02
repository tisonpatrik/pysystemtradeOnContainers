from pydantic import StringConstraints
from typing_extensions import Annotated

from common.src.http_client.requests.fetch_request import FetchRequest


class GetNormalizedPriceForAssetClassQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=15)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/normalized_prices_for_asset_class_router/get_normalized_prices_for_asset_class/"

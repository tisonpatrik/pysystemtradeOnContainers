from pydantic import StringConstraints
from typing_extensions import Annotated

from common.src.http_client.requests.fetch_request import FetchRequest


class NormalizedPriceForAssetClassQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/normalized_price_for_asset_class_route/get_normalized_price_for_asset_class/"

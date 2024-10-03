from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetNormalizedPriceForInstrumentQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=15)]

    @property
    def url_string(self) -> str:
        return "http://risk:8000/normalized_prices_for_instrument_route/get_normalized_prices_for_instrument/"

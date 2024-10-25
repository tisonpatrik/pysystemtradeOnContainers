from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetFxRateQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=30)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/fx_prices_route/get_fx_rate_by_symbol/"

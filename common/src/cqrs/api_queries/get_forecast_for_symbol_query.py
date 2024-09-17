from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetForecastForSymbolQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]

    @property
    def url_string(self) -> str:
        return "http://forecast:8000/get_forecast_for_instrument_route/get_forecast_for_instrument_async/"

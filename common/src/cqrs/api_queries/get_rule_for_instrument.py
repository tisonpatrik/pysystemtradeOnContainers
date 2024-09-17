from typing import Annotated

from pydantic import NonNegativeInt, StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetRuleForInstrumentQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]
    speed: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/get_accel_route/get_accel_for_instrument_async/"

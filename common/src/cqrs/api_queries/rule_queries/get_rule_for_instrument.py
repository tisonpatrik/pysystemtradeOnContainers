from typing import Annotated

from pydantic import NonNegativeInt, StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetRuleForInstrumentQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=30)]
    speed: NonNegativeInt
    use_attention: bool

    @property
    def url_string(self) -> str:
        return "http://rules:8000/rules_route/get_rule/"

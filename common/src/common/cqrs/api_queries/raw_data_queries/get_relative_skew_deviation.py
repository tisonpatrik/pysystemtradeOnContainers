from typing import Annotated

from pydantic import PositiveInt, StringConstraints

from common.http_client.requests.fetch_request import FetchRequest


class GetRelativeSkewDeviationQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=30)]
    lookback: PositiveInt

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/relative_skew_deviation_route/get_relative_skew_deviation/"

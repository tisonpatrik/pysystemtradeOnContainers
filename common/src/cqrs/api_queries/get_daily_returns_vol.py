from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetDailyReturnsVolQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=15)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/daily_returns_vol_route/get_daily_returns_vol/"

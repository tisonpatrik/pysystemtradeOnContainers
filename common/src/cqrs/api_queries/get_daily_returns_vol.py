from pydantic import StringConstraints
from typing_extensions import Annotated

from common.src.http_client.requests.fetch_request import FetchRequest


class GetDailyReturnsVolQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]

    @property
    def url_string(self) -> str:
        return "http://risk:8000/daily_returns_vol_route/get_daily_returns_vol/"

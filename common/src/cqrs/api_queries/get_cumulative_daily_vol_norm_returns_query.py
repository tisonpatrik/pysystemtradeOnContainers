from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class CumulativeDailyVolNormReturnsQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=30)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/cumulative_daily_vol_normalised_returns_route/get_cum_daily_vol_normalised_returns/"

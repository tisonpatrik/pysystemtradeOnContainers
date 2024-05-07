from pydantic import StringConstraints
from typing_extensions import Annotated

from common.src.http_client.requests.fetch_request import FetchRequest


class GetInstrumentCurrencyVolQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=10)]

    @property
    def url_string(self) -> str:
        return "http://risk:8000/instrument_currency_vol_route/get_instrument_currency_volatility/"

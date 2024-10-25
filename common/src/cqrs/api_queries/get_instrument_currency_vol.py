from typing import Annotated

from pydantic import StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest


class GetInstrumentCurrencyVolQuery(FetchRequest):
    symbol: Annotated[str, StringConstraints(max_length=30)]

    @property
    def url_string(self) -> str:
        return "http://raw_data:8000/instrument_currency_vol_route/get_instrument_currency_volatility/"

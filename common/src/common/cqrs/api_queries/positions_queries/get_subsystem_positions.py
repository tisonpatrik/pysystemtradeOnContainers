from typing import Annotated

from pydantic import PositiveFloat, StringConstraints

from common.http_client.requests.fetch_request import FetchRequest


class GetSubsystemPositionForInstrument(FetchRequest):
    notional_trading_capital: PositiveFloat
    percentage_volatility_target: PositiveFloat
    symbol: Annotated[str, StringConstraints(max_length=20)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]

    @property
    def url_string(self) -> str:
        return "http://rules:8000/get_accel_route/get_accel_for_instrument_async/"

from pydantic import BaseModel, PositiveFloat, StringConstraints, conlist
from typing_extensions import Annotated


class SubsystemPositionForInstrument(BaseModel):
    notional_trading_capital: PositiveFloat
    percentage_volatility_target: PositiveFloat
    avarage_absolute_forecas: PositiveFloat
    instrument_code: Annotated[str, StringConstraints(max_length=20)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]


class SubsystemPositionForListOfInstruments(BaseModel):
    notional_trading_capital: PositiveFloat
    percentage_volatility_target: PositiveFloat
    avarage_absolute_forecas: PositiveFloat
    instrument_codes: Annotated[list[str], conlist(str, min_length=1, max_length=500)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]

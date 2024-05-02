from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class GetFxRateQuery(BaseModel):
    symbol: Annotated[str, StringConstraints(max_length=10)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]

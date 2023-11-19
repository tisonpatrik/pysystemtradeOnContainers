from pydantic import BaseModel


class AdjustedPrices(BaseModel):

    directory = "/path/in/container/adjusted_prices_csv"

class FxPrices(BaseModel):

    directory = "/path/in/container/fx_prices_csv"

class MultiplePrices(BaseModel):

    directory = "/path/in/container/multiple_prices_csv"



class RollCalendars(BaseModel):

    directory = "/path/in/container/roll_calendars_csv"


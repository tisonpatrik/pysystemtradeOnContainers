import pandas as pd

from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key

NAME = "daily_returns"


class GetDailyReturnsCache(GetCacheStatement):
    def __init__(self, instrument_code: str):
        super().__init__(parameter=instrument_code)
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetDailyReturnsCache(SetCacheStatement):
    def __init__(self, returns: pd.Series, symbol: str):
        super().__init__(returns)
        self.instrument_code = symbol
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.instrument_code)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

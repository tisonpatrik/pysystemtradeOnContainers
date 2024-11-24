import pandas as pd

from common.redis.base_statements.get_cache_statement import GetCacheStatement
from common.redis.base_statements.set_cache_statement import SetCacheStatement
from common.utils.cache_utils import convert_datetime_to_unix, get_series_key

NAME = "negskew_cache"


class GetNegSkewCache(GetCacheStatement):
    def __init__(self, symbol: str, lookback: int):
        parameter = f"{symbol}_{lookback}"
        super().__init__(parameter=parameter)
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetNegSkewCache(SetCacheStatement):
    def __init__(self, negskew: pd.Series, symbol: str, lookback: int):
        super().__init__(negskew)
        self.parameter = f"{symbol}_{lookback}"
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

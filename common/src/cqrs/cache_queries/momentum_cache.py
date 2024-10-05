import pandas as pd

from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key

NAME = "momentum_cache"


class GetMomentumCache(GetCacheStatement):
    def __init__(self, symbol: str, speed: int):
        parameter = f"{symbol}_{speed}"
        super().__init__(parameter=parameter)
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetMomentumCache(SetCacheStatement):
    def __init__(self, signal: pd.Series, symbol: str, speed: int):
        super().__init__(signal)
        self.parameter = f"{symbol}_{speed}"
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

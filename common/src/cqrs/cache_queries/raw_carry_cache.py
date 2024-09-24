import pandas as pd

from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key


class GetRawCarryCache(GetCacheStatement):
    def __init__(self, symbol: str):
        super().__init__(parameter=symbol)
        self.name = "raw_carry_cache"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetRawCarryCache(SetCacheStatement):
    def __init__(self, daily_roll: pd.Series, symbol: str):
        super().__init__(daily_roll)
        self.asset_class = symbol
        self.name = "raw_carry_cache"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.asset_class)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

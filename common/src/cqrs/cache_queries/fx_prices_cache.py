import pandas as pd

from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key

NAME = "fx_prices"


class GetFxPricesCache(GetCacheStatement):
    def __init__(self, key: str):
        super().__init__(parameter=key)
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetFxPricesCache(SetCacheStatement):
    def __init__(self, values: pd.Series, key: str):
        super().__init__(values)
        self.symbol = key
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.symbol)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

import pandas as pd

from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key


class GetDailyReturnsVolCache(GetCacheStatement):
    def __init__(self, instrument_code: str):
        super().__init__(parameter=instrument_code)
        self.name = "daily_returns_vol"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetDailyReturnsVolCache(SetCacheStatement):
    def __init__(self, vol: pd.Series, instrument_code: str):
        super().__init__(vol)
        self.instrument_code = instrument_code
        self.name = "daily_returns_vol"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.instrument_code)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

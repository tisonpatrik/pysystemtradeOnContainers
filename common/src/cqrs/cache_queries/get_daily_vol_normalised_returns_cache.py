from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.utils.cache_utils import get_series_key

class GetDailyvolNormalizedReturnsCache(GetCacheStatement):
    def __init__(self, instrument_code: str):
        super().__init__(parameter = instrument_code)
        self.name = "daily_vol_normalised_returns"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)

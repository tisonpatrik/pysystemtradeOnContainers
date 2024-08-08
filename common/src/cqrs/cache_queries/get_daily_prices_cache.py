from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.utils.cache_utils import get_series_key

class GetDailyPricesCache(GetCacheStatement):
    def __init__(self, instrument_code: str):
        super().__init__(instrument_code)
        self.name = "daily_prices"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.instrument_code)

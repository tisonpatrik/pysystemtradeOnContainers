import pandas as pd
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import get_series_key

class SetDailyPricesCache(SetCacheStatement):
    def __init__(self, prices: pd.Series, instrument_code: str):
        super().__init__(prices)
        self.instrument_code = instrument_code
        self.name = "daily_prices"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.instrument_code)

    @property
    def cache_value(self) -> dict:
        return self.values.to_dict()

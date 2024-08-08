import pandas as pd
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import get_series_key
from common.src.utils.cache_utils import convert_datetime_to_unix

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
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

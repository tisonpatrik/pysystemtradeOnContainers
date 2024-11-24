import pandas as pd

from common.redis.base_statements.get_cache_statement import GetCacheStatement
from common.redis.base_statements.set_cache_statement import SetCacheStatement
from common.utils.cache_utils import convert_datetime_to_unix, get_series_key

NAME = "normalized_price_for_asset_class"


class GetNormalizedPriceForAssetClassCache(GetCacheStatement):
    def __init__(self, symbol: str):
        super().__init__(parameter=symbol)
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)


class SetNormalizedPriceForAssetClassCache(SetCacheStatement):
    def __init__(self, prices: pd.Series, symbol: str):
        super().__init__(prices)
        self.asset_class = symbol
        self.name = NAME

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.asset_class)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

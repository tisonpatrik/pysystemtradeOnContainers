from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.utils.cache_utils import get_series_key

class GetAggregatedReturnsForAssetClassCache(GetCacheStatement):
    def __init__(self, asset_class: str):
        super().__init__(parameter = asset_class)
        self.name = "aggregated_returns_for_asset_class"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.parameter)

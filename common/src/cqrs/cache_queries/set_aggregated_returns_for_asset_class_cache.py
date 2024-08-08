import pandas as pd

from common.src.redis.base_statements.set_cache_statement import SetCacheStatement
from common.src.utils.cache_utils import convert_datetime_to_unix, get_series_key


class SetAggregatedReturnsForAssetClassCache(SetCacheStatement):
    def __init__(self, returns: pd.DataFrame, asset_class: str):
        super().__init__(returns)
        self.asset_class = asset_class
        self.name = "aggregated_returns_for_asset_class"

    @property
    def cache_key(self) -> str:
        return get_series_key(self.name, self.asset_class)

    @property
    def cache_value(self) -> dict:
        series = convert_datetime_to_unix(self.values)
        return series.to_dict()

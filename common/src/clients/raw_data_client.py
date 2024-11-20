import asyncio
from asyncio import Task

import pandas as pd

from common.src.cqrs.api_queries.raw_data_queries.get_absolute_skew_deviation import GetAbsoluteSkewDeviationQuery
from common.src.cqrs.api_queries.raw_data_queries.get_cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturnsQuery
from common.src.cqrs.api_queries.raw_data_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.cqrs.api_queries.raw_data_queries.get_fx_prices import GetFxPricesQuery
from common.src.cqrs.api_queries.raw_data_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.cqrs.api_queries.raw_data_queries.get_normalized_price_for_asset_class import GetNormalizedPriceForAssetClassQuery
from common.src.cqrs.api_queries.raw_data_queries.get_relative_skew_deviation import GetRelativeSkewDeviationQuery
from common.src.cqrs.api_queries.raw_data_queries.get_vol_attenuation import GetVolAttenuationQuery
from common.src.cqrs.cache_queries.cumulative_daily_vol_norm_returns_cache import (
    GetCumulativeDailyVolNormReturnsCache,
    SetCumulativeDailyVolNormReturnsCache,
)
from common.src.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.src.cqrs.cache_queries.fx_prices_cache import GetFxPricesCache, SetFxPricesCache
from common.src.cqrs.cache_queries.normalized_price_for_asset_class_cache import (
    GetNormalizedPriceForAssetClassCache,
    SetNormalizedPriceForAssetClassCache,
)
from common.src.cqrs.cache_queries.vol_attenuation_cache import GetVolAttenuationCache, SetVolAttenuationCache
from common.src.http_client.rest_client import RestClient
from common.src.redis.redis_repository import RedisRepository
from common.src.validation.absolute_skew_deviation import AbsoluteSkewDeviation
from common.src.validation.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from common.src.validation.daily_returns_vol import DailyReturnsVol
from common.src.validation.fx_prices import FxPrices
from common.src.validation.instrument_currency_vol import InstrumentCurrencyVol
from common.src.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass
from common.src.validation.relative_skew_deviation import RelativeSkewDeviation
from common.src.validation.vol_attenuation import VolAttenuation


class RawDataClient:
    def __init__(self, rest_client: RestClient, redis_repository: RedisRepository):
        self.client = rest_client
        self.redis_repository = redis_repository
        self.background_tasks: set[Task] = set()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDailyReturnsVolCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return DailyReturnsVol.from_cache_to_series(cached_data)
        query = GetDailyReturnsVolQuery(symbol=symbol)
        vol_data = await self.client.get_data_async(query)
        vol = DailyReturnsVol.from_api_to_series(vol_data)

        cache_set_statement = SetDailyReturnsVolCache(vol=vol, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return vol

    async def get_normalized_prices_for_asset_class_async(self, symbol: str) -> pd.Series:
        cache_statement = GetNormalizedPriceForAssetClassCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return NormalizedPricesForAssetClass.from_cache_to_series(cached_data)
        query = GetNormalizedPriceForAssetClassQuery(symbol=symbol)
        raw_data = await self.client.get_data_async(query)
        data = NormalizedPricesForAssetClass.from_api_to_series(raw_data)
        cache_set_statement = SetNormalizedPriceForAssetClassCache(prices=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def get_cumulative_daily_vol_normalised_returns_async(self, symbol: str) -> pd.Series:
        cache_statement = GetCumulativeDailyVolNormReturnsCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return CumulativeDailyVolNormReturns.from_cache_to_series(cached_data)
        query = CumulativeDailyVolNormReturnsQuery(symbol=symbol)
        raw_data = await self.client.get_data_async(query)
        data = CumulativeDailyVolNormReturns.from_api_to_series(raw_data)
        cache_set_statement = SetCumulativeDailyVolNormReturnsCache(prices=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def absolute_skew_deviation_async(self, symbol: str, lookback: int) -> pd.Series:
        query = GetAbsoluteSkewDeviationQuery(symbol=symbol, lookback=lookback)
        raw_data = await self.client.get_data_async(query)
        return AbsoluteSkewDeviation.from_api_to_series(raw_data)

    async def relative_skew_deviation_async(self, symbol: str, lookback: int) -> pd.Series:
        query = GetRelativeSkewDeviationQuery(symbol=symbol, lookback=lookback)
        raw_data = await self.client.get_data_async(query)
        return RelativeSkewDeviation.from_api_to_series(raw_data)

    async def get_vol_attenutation_async(self, symbol: str) -> pd.Series:
        cache_statement = GetVolAttenuationCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return VolAttenuation.from_cache_to_series(cached_data)
        query = GetVolAttenuationQuery(symbol=symbol)
        raw_data = await self.client.get_data_async(query)
        data = VolAttenuation.from_api_to_series(raw_data)
        cache_set_statement = SetVolAttenuationCache(values=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def get_instrument_volatility_async(self, symbol: str) -> pd.Series:
        get_instrument_vol_query = GetInstrumentCurrencyVolQuery(symbol=symbol)
        raw_data = await self.client.get_data_async(get_instrument_vol_query)
        return InstrumentCurrencyVol.from_api_to_series(raw_data)

    async def get_fx_prices_async(self, symbol: str, base_currency: str) -> pd.Series:
        key = f"{symbol}_{base_currency}"
        cache_statement = GetFxPricesCache(key)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return FxPrices.from_cache_to_series(cached_data)
        query = GetFxPricesQuery(symbol=symbol, base_currency=base_currency)
        raw_data = await self.client.get_data_async(query)
        data = FxPrices.from_api_to_series(raw_data)
        cache_set_statement = SetFxPricesCache(values=data, key=key)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

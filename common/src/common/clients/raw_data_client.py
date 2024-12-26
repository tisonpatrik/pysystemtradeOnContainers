# raw_data_client.py

import asyncio
from asyncio import Task

import pandas as pd
from grpc.aio import AioRpcError, Channel

from common.cqrs.cache_queries.cumulative_daily_vol_norm_returns_cache import (
    GetCumulativeDailyVolNormReturnsCache,
    SetCumulativeDailyVolNormReturnsCache,
)
from common.cqrs.cache_queries.daily_returns_vol_cache import GetDailyReturnsVolCache, SetDailyReturnsVolCache
from common.cqrs.cache_queries.normalized_price_for_asset_class_cache import (
    GetNormalizedPriceForAssetClassCache,
    SetNormalizedPriceForAssetClassCache,
)
from common.cqrs.cache_queries.vol_attenuation_cache import GetVolAttenuationCache, SetVolAttenuationCache
from common.protobufs.raw_data_pb2 import (
    AbsoluteSkewDeviationRequest,
    CumulativeDailyVolNormReturnsRequest,
    DailyReturnsVolRequest,
    NormalizedPricesRequest,
    RelativeSkewDeviationRequest,
    VolAttenuationRequest,
)
from common.protobufs.raw_data_pb2_grpc import (
    AbsoluteSkewDeviationStub,
    CumulativeDailyVolNormReturnsStub,
    DailyReturnsVolStub,
    NormalizedPricesStub,
    RelativeSkewDeviationStub,
    VolAttenuationStub,
)
from common.redis.redis_repository import RedisClient
from common.validation.absolute_skew_deviation import AbsoluteSkewDeviation
from common.validation.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from common.validation.daily_returns_vol import DailyReturnsVol
from common.validation.normalized_prices_for_asset_class import NormalizedPricesForAssetClass
from common.validation.relative_skew_deviation import RelativeSkewDeviation
from common.validation.vol_attenuation import VolAttenuation


class RawDataClient:
    def __init__(self, grpc_channel: Channel, redis_repository: RedisClient):
        self.daily_returns_vol_stub = DailyReturnsVolStub(grpc_channel)
        self.cumulative_daily_vol_norm_returns_stub = CumulativeDailyVolNormReturnsStub(grpc_channel)
        self.vol_atenuation_stub = VolAttenuationStub(grpc_channel)
        self.normalized_prices_stub = NormalizedPricesStub(grpc_channel)
        self.absolute_skew_deviation_stub = AbsoluteSkewDeviationStub(grpc_channel)
        self.relative_skew_deviation_stub = RelativeSkewDeviationStub(grpc_channel)
        self.redis_repository = redis_repository
        self.background_tasks: set[Task] = set()

    async def get_daily_returns_vol_async(self, symbol: str) -> pd.Series:
        cache_statement = GetDailyReturnsVolCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return DailyReturnsVol.from_cache_to_series(cached_data)

        request = DailyReturnsVolRequest(symbol=symbol)

        try:
            response = await self.daily_returns_vol_stub.get_daily_returns_vol(request)
        except AioRpcError as e:
            raise e

        data = DailyReturnsVol.from_api_to_series(response.series)

        cache_set_statement = SetDailyReturnsVolCache(vol=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))
        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def get_normalized_prices_for_asset_class_async(self, symbol: str) -> pd.Series:
        cache_statement = GetNormalizedPriceForAssetClassCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return NormalizedPricesForAssetClass.from_cache_to_series(cached_data)

        request = NormalizedPricesRequest(symbol=symbol)
        try:
            response = await self.normalized_prices_stub.get_normalized_prices(request)
        except AioRpcError as e:
            raise e
        data = NormalizedPricesForAssetClass.from_api_to_series(response.series)

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

        request = CumulativeDailyVolNormReturnsRequest(symbol=symbol)
        try:
            response = await self.cumulative_daily_vol_norm_returns_stub.get_cumulative_daily_vol_norm_returns(request)
        except AioRpcError as e:
            raise e

        data = CumulativeDailyVolNormReturns.from_api_to_series(response.series)

        cache_set_statement = SetCumulativeDailyVolNormReturnsCache(prices=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def get_vol_attenutation_async(self, symbol: str) -> pd.Series:
        cache_statement = GetVolAttenuationCache(symbol)
        cached_data = await self.redis_repository.get_cache(cache_statement)
        if cached_data is not None:
            return VolAttenuation.from_cache_to_series(cached_data)

        request = VolAttenuationRequest(symbol=symbol)
        try:
            response = await self.vol_atenuation_stub.get_vol_attenuation(request)
        except AioRpcError as e:
            raise e

        data = VolAttenuation.from_api_to_series(response.series)
        cache_set_statement = SetVolAttenuationCache(values=data, symbol=symbol)
        cache_task = asyncio.create_task(self.redis_repository.set_cache(cache_set_statement))

        self.background_tasks.add(cache_task)
        cache_task.add_done_callback(self.background_tasks.discard)
        return data

    async def absolute_skew_deviation_async(self, symbol: str, lookback: int) -> pd.Series:
        request = AbsoluteSkewDeviationRequest(symbol=symbol, lookback=lookback)
        try:
            response = await self.absolute_skew_deviation_stub.get_absolute_skew_deviation(request)
        except AioRpcError as e:
            raise e
        return AbsoluteSkewDeviation.from_api_to_series(response.series)

    async def relative_skew_deviation_async(self, symbol: str, lookback: int) -> pd.Series:
        request = RelativeSkewDeviationRequest(symbol=symbol, lookback=lookback)
        try:
            response = await self.relative_skew_deviation_stub.get_relative_skew_deviation(request)
        except AioRpcError as e:
            raise e
        return RelativeSkewDeviation.from_api_to_series(response.series)

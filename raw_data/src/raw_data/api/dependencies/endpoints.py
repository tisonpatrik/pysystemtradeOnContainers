from common.clients.dependencies import get_database_async
from common.database.repository import PostgresClient

from raw_data.api.dependencies.handlers import (
    HandlerFactory,
)
from raw_data.api.endpoints.absolute_skew_deviation import AbsoluteSkewDeviation
from raw_data.api.endpoints.cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturns
from raw_data.api.endpoints.daily_returns_vol import DailyReturnsVol
from raw_data.api.endpoints.fx_prices import FxPrices
from raw_data.api.endpoints.instrument_currency_vol import InstrumentCurrencyVol
from raw_data.api.endpoints.median_carry import MedianCarry
from raw_data.api.endpoints.normalized_prices import NormalizedPrices
from raw_data.api.endpoints.raw_carry import RawCarry
from raw_data.api.endpoints.relative_skew_deviation import RelativeSkewDeviation
from raw_data.api.endpoints.smooth_carry import SmoothCarry
from raw_data.api.endpoints.vol_attenuation import VolAttenuation


class EndpointFactory:
    def __init__(self, postgres: PostgresClient):
        self.postgres = postgres
        self.handler_factory = HandlerFactory(self.postgres)

    @staticmethod
    async def create() -> 'EndpointFactory':
        postgres = await get_database_async()
        return EndpointFactory(postgres=postgres)

    def get_absolute_skew_deviation(self) -> AbsoluteSkewDeviation:
        handler = self.handler_factory.get_absolute_skew_deviation_handler()
        return AbsoluteSkewDeviation(absolute_skew_deviation_handler=handler)

    def get_fx_prices(self) -> FxPrices:
        handler = self.handler_factory.get_fx_prices_handler()
        return FxPrices(fx_prices_handler=handler)

    def get_daily_returns_vol(self) -> DailyReturnsVol:
        handler = self.handler_factory.get_daily_returns_vol_handler()
        return DailyReturnsVol(daily_returns_vol_handler=handler)

    def get_instrument_currency_vol(self) -> InstrumentCurrencyVol:
        handler = self.handler_factory.get_instrument_currency_vol_handler()
        return InstrumentCurrencyVol(instrument_currency_vol_handler=handler)

    def get_vol_attenuation(self) -> VolAttenuation:
        handler = self.handler_factory.get_vol_attenuation_handler()
        return VolAttenuation(vol_attenuation_handler=handler)

    def get_relative_skew_deviation(self) -> RelativeSkewDeviation:
        handler = self.handler_factory.get_relative_skew_deviation_handler()
        return RelativeSkewDeviation(relative_skew_deviation_handler=handler)

    def get_cumulative_daily_vol_norm_returns(self) -> CumulativeDailyVolNormReturns:  # noqa: F821
        handler = self.handler_factory.get_cumulative_daily_vol_norm_returns_handler()
        return CumulativeDailyVolNormReturns(cumulative_daily_vol_norm_returns_handler=handler)

    def get_raw_carry(self) -> RawCarry:
        handler = self.handler_factory.get_raw_carry_handler()
        return RawCarry(raw_carry_handler=handler)

    def get_median_carry_for_asset_class(self) -> MedianCarry:
        handler = self.handler_factory.get_median_carry_for_asset_class_handler()
        return MedianCarry(median_carry_for_asset_class_handler=handler)

    def get_smooth_carry(self) -> SmoothCarry:
        handler = self.handler_factory.get_smooth_carry_handler()
        return SmoothCarry(smooth_carry_handler=handler)

    def get_normalized_prices(self) -> NormalizedPrices:
        handler = self.handler_factory.get_normalized_prices_handler()
        return NormalizedPrices(normalized_prices_handler=handler)

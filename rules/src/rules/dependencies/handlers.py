from common.clients.dependencies import get_redis
from common.clients.old_carry_client import CarryClient
from common.clients.old_dependencies import (
    get_carry_client,
    get_daily_prices_client,
    get_raw_data_client,
)
from common.clients.prices_client import PricesClient
from common.clients.raw_data_client import RawDataClient

from rules.api.accel.handler import AccelHandler
from rules.api.handlers.asserttrend_handler import AssertTrendHandler
from rules.api.handlers.attenutation_handler import AttenutationHandler
from rules.api.handlers.breakout_handler import BreakoutHandler
from rules.api.handlers.carry_handler import CarryHandler
from rules.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler
from rules.api.handlers.momentum_handler import MomentumHandler
from rules.api.handlers.momentum_rule_handler import MomentumRuleHandler
from rules.api.handlers.normalized_momentum_handler import NormalizedMomentumHandler
from rules.api.handlers.relative_carry_handler import RelativeCarryHandler
from rules.api.handlers.relative_momentum_handler import RelativeMomentumHandler
from rules.api.handlers.skewabs_handler import SkewAbsHandler
from rules.api.handlers.skewrel_handler import SkewRelHandler


class HandlerFactory:
    def __init__(self):
        self.redis = get_redis()
        self.raw_data_client: RawDataClient = get_raw_data_client()
        self.prices_client: PricesClient = get_daily_prices_client()
        self.carry_client: CarryClient = get_carry_client()
        self.attenuation_handler: AttenutationHandler = AttenutationHandler(raw_data_client=self.raw_data_client)

    def get_momentum_handler(self) -> MomentumHandler:
        return MomentumHandler(prices_client=self.prices_client, raw_data_client=self.raw_data_client, redis=self.redis)

    def get_normalized_momentum_handler(self) -> NormalizedMomentumHandler:
        return NormalizedMomentumHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

    def get_momentum_rule_handler(self) -> MomentumRuleHandler:
        return MomentumRuleHandler(momentum_handler=self.get_momentum_handler(), attenuation_handler=self.attenuation_handler)

    def get_accel_handler(self) -> AccelHandler:
        return AccelHandler(momentum_handler=self.get_momentum_handler(), attenuation_handler=self.attenuation_handler)

    def get_breakout_handler(self) -> BreakoutHandler:
        return BreakoutHandler(prices_client=self.prices_client, attenuation_handler=self.attenuation_handler)

    def get_asserttrend_handler(self) -> AssertTrendHandler:
        return AssertTrendHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

    def get_carry_handler(self) -> CarryHandler:
        return CarryHandler(carry_client=self.carry_client, attenuation_handler=self.attenuation_handler)

    def get_cs_mean_reversion_handler(self) -> CSMeanReversionHandler:
        return CSMeanReversionHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

    def get_relative_carry_handler(self) -> RelativeCarryHandler:
        return RelativeCarryHandler(carry_client=self.carry_client, attenuation_handler=self.attenuation_handler)

    def get_relative_momentum_handler(self) -> RelativeMomentumHandler:
        return RelativeMomentumHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

    def get_skewabs_handler(self) -> SkewAbsHandler:
        return SkewAbsHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

    def get_skewrel_handler(self) -> SkewRelHandler:
        return SkewRelHandler(raw_data_client=self.raw_data_client, attenuation_handler=self.attenuation_handler)

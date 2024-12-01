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
from rules.api.asserttrend.handler import AssertTrendHandler
from rules.api.breakout.handler import BreakoutHandler
from rules.api.carry.handler import CarryHandler
from rules.api.csmeanreversion.handler import CSMeanReversionHandler
from rules.api.momentum.handler import MomentumRuleHandler
from rules.api.normalized_momentum.handler import NormalizedMomentumHandler
from rules.api.relative_carry.handler import RelativeCarryHandler
from rules.api.relative_momentum.handler import RelativeMomentumHandler
from rules.api.skewabs.handler import SkewAbsHandler
from rules.api.skewrel.handler import SkewRelHandler
from rules.shared.attenutation_handler import AttenutationHandler
from rules.shared.momentum_handler import MomentumHandler


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

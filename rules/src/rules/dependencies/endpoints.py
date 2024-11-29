from rules.api.accel.endpoint import Accel
from rules.api.endpoints.assettrend import AssertTrend
from rules.api.endpoints.breakout import Breakout
from rules.api.endpoints.carry import Carry
from rules.api.endpoints.cs_mean_reversion import CSMeanReversion
from rules.dependencies.handlers import HandlerFactory


class EndpointFactory:
    def __init__(self):
        self.handler_factory = HandlerFactory()

    def get_accel(self) -> Accel:
        accel_handler = self.handler_factory.get_accel_handler()
        return Accel(accel_handler=accel_handler)

    def get_asserttrend(self) -> AssertTrend:
        asserttrend_handler = self.handler_factory.get_asserttrend_handler()
        return AssertTrend(asserttrend_handler=asserttrend_handler)

    def get_breakout(self) -> Breakout:
        breakout_handler = self.handler_factory.get_breakout_handler()
        return Breakout(breakout_handler=breakout_handler)

    def get_carry(self) -> Carry:
        carry_handler = self.handler_factory.get_carry_handler()
        return Carry(carry_handler=carry_handler)

    def get_csmeanreversion(self) -> CSMeanReversion:
        csmeanreversion_handler = self.handler_factory.get_cs_mean_reversion_handler()
        return CSMeanReversion(csmeanreversion_handler=csmeanreversion_handler)

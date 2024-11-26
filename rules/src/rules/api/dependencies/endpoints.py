from rules.api.dependencies.handlers import HandlerFactory
from rules.api.endpoints.accel import Accel
from rules.api.endpoints.assettrend import AssertTrend
from rules.api.endpoints.breakout import Breakout


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

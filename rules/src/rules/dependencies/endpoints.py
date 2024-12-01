from rules.api.rules_processor.enpoint import RulesProcessor
from rules.dependencies.handlers import HandlerFactory


class EndpointFactory:
    def __init__(self):
        self.handler_factory = HandlerFactory()

    def get_rules_processor(self):
        accel_handler = self.handler_factory.get_accel_handler()
        assert_trend_handler = self.handler_factory.get_asserttrend_handler()
        breakout_handler = self.handler_factory.get_breakout_handler()
        carry_handler = self.handler_factory.get_carry_handler()
        csmeanreversion_handler = self.handler_factory.get_cs_mean_reversion_handler()
        momentum_handler = self.handler_factory.get_momentum_rule_handler()
        normalized_momentum_handler = self.handler_factory.get_normalized_momentum_handler()
        relative_carry_handler = self.handler_factory.get_relative_carry_handler()
        relative_momentum_handler = self.handler_factory.get_relative_momentum_handler()
        skewabs_handler = self.handler_factory.get_skewabs_handler()
        skewrel_handler = self.handler_factory.get_skewrel_handler()

        return RulesProcessor(
            accel_handler=accel_handler,
            assert_trend_handler=assert_trend_handler,
            breakout_handler=breakout_handler,
            carry_handler=carry_handler,
            cs_mean_reversion_handler=csmeanreversion_handler,
            momentum_handler=momentum_handler,
            normalized_momentum_handler=normalized_momentum_handler,
            relative_carry_handler=relative_carry_handler,
            relative_momentum_handler=relative_momentum_handler,
            skewabs_handler=skewabs_handler,
            skewrel_handler=skewrel_handler,
        )

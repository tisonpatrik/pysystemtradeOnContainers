import pandas as pd
from common.logging.logger import AppLogger
from common.protobufs.rules_processor_pb2 import RulesBatchRequest, RulesBatchResponse
from common.protobufs.rules_processor_pb2_grpc import RulesProcessorServicer
from common.utils.convertors import convert_pandas_to_bytes
from grpc import ServicerContext, StatusCode

from rules.api.accel.handler import AccelHandler
from rules.api.accel.request import AccelQuery
from rules.api.asserttrend.handler import AssertTrendHandler
from rules.api.asserttrend.request import AssetTrendQuery
from rules.api.breakout.handler import BreakoutHandler
from rules.api.breakout.request import BreakoutQuery
from rules.api.carry.handler import CarryHandler
from rules.api.carry.request import CarryQuery
from rules.api.csmeanreversion.handler import CSMeanReversionHandler
from rules.api.csmeanreversion.request import CSMeanReversionQuery
from rules.api.momentum.handler import MomentumRuleHandler
from rules.api.momentum.request import MomentumQuery
from rules.api.normalized_momentum.handler import NormalizedMomentumHandler
from rules.api.normalized_momentum.request import NormalizedMomentumQuery
from rules.api.relative_carry.handler import RelativeCarryHandler
from rules.api.relative_carry.request import RelativeCarryQuery
from rules.api.relative_momentum.handler import RelativeMomentumHandler
from rules.api.relative_momentum.request import RelativeMomentumQuery
from rules.api.skewabs.handler import SkewAbsHandler
from rules.api.skewabs.request import SkewAbsQuery
from rules.api.skewrel.handler import SkewRelHandler
from rules.api.skewrel.request import SkewRelQuery
from rules.utils.rule_query_factory import RuleQueryFactory


class RulesProcessor(RulesProcessorServicer):
    def __init__(
        self,
        accel_handler: AccelHandler,
        assert_trend_handler: AssertTrendHandler,
        breakout_handler: BreakoutHandler,
        carry_handler: CarryHandler,
        cs_mean_reversion_handler: CSMeanReversionHandler,
        momentum_handler: MomentumRuleHandler,
        normalized_momentum_handler: NormalizedMomentumHandler,
        relative_carry_handler: RelativeCarryHandler,
        relative_momentum_handler: RelativeMomentumHandler,
        skewabs_handler: SkewAbsHandler,
        skewrel_handler: SkewRelHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.rule_query_factory = RuleQueryFactory()

        self.accel_handler = accel_handler
        self.assert_trend_handler = assert_trend_handler
        self.breakout_handler = breakout_handler
        self.carry_handler = carry_handler
        self.cs_mean_reversion_handler = cs_mean_reversion_handler
        self.momentum_handler = momentum_handler
        self.normalized_momentum_handler = normalized_momentum_handler
        self.relative_carry_handler = relative_carry_handler
        self.relative_momentum_handler = relative_momentum_handler
        self.skewabs_handler = skewabs_handler
        self.skewrel_handler = skewrel_handler

    async def process_rules(self, request: RulesBatchRequest, context: ServicerContext) -> RulesBatchResponse:
        self.logger.info('Processing batch of %d rules', len(request.rules))

        combined_results = []
        for rule_request in request.rules:
            try:
                # Create the appropriate query using the factory
                query = self.rule_query_factory.create_rule_query(rule_request)

                # Dispatch to the appropriate handler based on query type
                if isinstance(query, AccelQuery):
                    results = await self.accel_handler.get_accel_async(query)
                elif isinstance(query, AssetTrendQuery):
                    results = await self.assert_trend_handler.get_asserttrend_async(query)
                elif isinstance(query, BreakoutQuery):
                    results = await self.breakout_handler.get_breakout_async(query)
                elif isinstance(query, CarryQuery):
                    results = await self.carry_handler.get_carry_async(query)
                elif isinstance(query, CSMeanReversionQuery):
                    results = await self.cs_mean_reversion_handler.get_cs_mean_reversion_async(query)
                elif isinstance(query, MomentumQuery):
                    results = await self.momentum_handler.get_momentum_async(query)
                elif isinstance(query, NormalizedMomentumQuery):
                    results = await self.normalized_momentum_handler.get_normalized_momentum_async(query)
                elif isinstance(query, RelativeCarryQuery):
                    results = await self.relative_carry_handler.get_relative_carry_async(query)
                elif isinstance(query, RelativeMomentumQuery):
                    results = await self.relative_momentum_handler.get_relative_momentum_async(query)
                elif isinstance(query, SkewAbsQuery):
                    results = await self.skewabs_handler.get_skewabs_async(query)
                elif isinstance(query, SkewRelQuery):
                    results = await self.skewrel_handler.get_skewrel_async(query)
                else:
                    self.logger.warning('Unrecognized query type in factory dispatch.')
                    continue

                # Convert results to bytes and add to the combined results
                combined_results.append(results)

            except Exception as e:
                self.logger.exception('Error processing rule: %s', str(e))
                context.abort(StatusCode.INTERNAL, f'An error occurred while processing a rule: {str(e)}')

        # Combine all results into a single response
        combined_frame = pd.concat(combined_results, axis=1)
        bytes = convert_pandas_to_bytes(combined_frame)
        return RulesBatchResponse(series=bytes)

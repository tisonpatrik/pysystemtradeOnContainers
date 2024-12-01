from common.cqrs.api_queries.rule_queries.get_breakout import GetBreakoutQuery
from common.cqrs.api_queries.rule_queries.get_carry import GetCarryQuery
from common.cqrs.api_queries.rule_queries.get_cross_sectional_mean_reversion import GetCrossSectionalMeanReversionQuery
from common.cqrs.api_queries.rule_queries.get_momentum import GetMomentumQuery
from common.protobufs.rules_processor_pb2 import Accel, AssertTrend, Breakout, Carry, CSMeanReversion, Momentum, RuleRequest
from common.validation.scaling_type import ScalingType

from rules.api.accel.request import AccelQuery
from rules.api.asserttrend.request import AssetTrendQuery
from rules.validation.base_rule_request import BaseRuleRequest


class RuleQueryFactory:
    _query_map = {
        Accel: AccelQuery,
        AssertTrend: AssetTrendQuery,
        Breakout: GetBreakoutQuery,
        Carry: GetCarryQuery,
        CSMeanReversion: GetCrossSectionalMeanReversionQuery,
        # 'normmom': GetNormalizedMomentumQuery,
        Momentum: GetMomentumQuery,
        # 'relative_carry': GetRelativeCarry,
        # 'relative_momentum': GetRelativeMomentumQuery,
        # 'skewabs': GetSkewAbsQuery,
        # 'skewrv': GetSkewRelQuery,
        # Add new mappings here as needed
    }

    def __init__(self):
        self.scaling_type = ScalingType.FIXED

    def create_rule_query(self, grpc_request: RuleRequest) -> BaseRuleRequest:
        # Get the type of rule (e.g., "Accel", "AssertTrend")
        rule_type = grpc_request.WhichOneof('rule')

        # Validate the rule type exists in the map
        if not rule_type:
            raise ValueError('No valid rule type provided in RuleRequest.')

        # Get the corresponding query class from the map
        query_class = self._query_map.get(getattr(RuleRequest, rule_type).DESCRIPTOR.full_name)

        if not query_class:
            raise ValueError(f'Unknown rule type: {rule_type}')

        # Extract the rule parameters
        grpc_rule = getattr(grpc_request, rule_type)

        # Construct the query object
        return query_class(
            symbol=grpc_rule.symbol,
            scaling_type=self.scaling_type.value,
            scaling_factor=grpc_rule.scaling_factor,
            use_attenuation=grpc_rule.use_attenuation,
            **self._extract_rule_parameters(grpc_rule),
        )

    @staticmethod
    def _extract_rule_parameters(grpc_rule) -> dict:
        """Extract all fields from the gRPC rule message."""
        return {
            field.name: getattr(grpc_rule, field.name)
            for field in grpc_rule.DESCRIPTOR.fields
            if field.name not in {'symbol', 'scaling_type', 'scaling_factor', 'use_attenuation'}
        }

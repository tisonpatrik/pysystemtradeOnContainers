from common.src.cqrs.api_queries.rule_queries.get_accel import GetAccelQuery
from common.src.cqrs.api_queries.rule_queries.get_assettrend import GetAssetTrendQuery
from common.src.cqrs.api_queries.rule_queries.get_breakout import GetBreakoutQuery
from common.src.cqrs.api_queries.rule_queries.get_carry import GetCarryQuery
from common.src.cqrs.api_queries.rule_queries.get_cross_sectional_mean_reversion import GetCrossSectionalMeanReversionQuery
from common.src.cqrs.api_queries.rule_queries.get_momentum import GetMomentumQuery
from common.src.cqrs.api_queries.rule_queries.get_normalized_momentum import GetNormalizedMomentumQuery
from common.src.cqrs.api_queries.rule_queries.get_relative_carry import GetRelativeCarry
from common.src.cqrs.api_queries.rule_queries.get_relative_momentum import GetRelativeMomentumQuery
from common.src.cqrs.api_queries.rule_queries.get_skewabs import GetSkewAbsQuery
from common.src.cqrs.api_queries.rule_queries.get_skewrel import GetSkewRelQuery
from common.src.cqrs.api_queries.rule_queries.rule_request import RuleRequest
from common.src.validation.rule import Rule
from common.src.validation.scaling_type import ScalingType


class RuleQueryFactory:
    _query_map = {
        "breakout": GetBreakoutQuery,
        "relative_momentum": GetRelativeMomentumQuery,
        "skewrv": GetSkewRelQuery,
        "cross_sectional_mean_reversion": GetCrossSectionalMeanReversionQuery,
        "carry": GetCarryQuery,
        "assettrend": GetAssetTrendQuery,
        "normmom": GetNormalizedMomentumQuery,
        "momentum": GetMomentumQuery,
        "relative_carry": GetRelativeCarry,
        "skewabs": GetSkewAbsQuery,
        "accel": GetAccelQuery,
        # Add new mappings here as needed
    }

    def __init__(self, scaling_type: ScalingType):
        self.scaling_type = scaling_type

    def create_rule_query(self, symbol: str, rule: Rule) -> RuleRequest:
        query_class = self._query_map.get(rule.rule_name)

        if not query_class:
            raise ValueError(f"Unknown rule variation: {rule.rule_name}")

        return query_class(
            symbol=symbol,
            scaling_type=self.scaling_type.value,
            scaling_factor=rule.scaling_factor,
            use_attenuation=rule.use_attenuation,
            **rule.rule_parameters,
        )

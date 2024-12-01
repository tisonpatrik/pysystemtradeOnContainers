from pydantic import NonNegativeInt

from rules.validation.base_rule_request import BaseRuleRequest


class SkewAbsQuery(BaseRuleRequest):
    smooth: NonNegativeInt
    lookback: NonNegativeInt
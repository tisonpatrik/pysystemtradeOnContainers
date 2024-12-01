from pydantic import NonNegativeInt

from rules.validation.base_rule_request import BaseRuleRequest


class CarryQuery(BaseRuleRequest):
    smooth_days: NonNegativeInt

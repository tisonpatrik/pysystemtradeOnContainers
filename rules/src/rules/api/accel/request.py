from pydantic import NonNegativeInt

from rules.validation.base_rule_request import BaseRuleRequest


class AccelQuery(BaseRuleRequest):
    lfast: NonNegativeInt
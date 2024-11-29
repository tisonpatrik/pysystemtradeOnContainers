from pydantic import NonNegativeInt

from rules.validation.rule_request import RuleRequest


class AccelQuery(RuleRequest):
    lfast: NonNegativeInt

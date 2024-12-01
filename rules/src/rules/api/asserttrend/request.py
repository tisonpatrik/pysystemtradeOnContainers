from pydantic import NonNegativeInt

from rules.validation.base_rule_request import BaseRuleRequest


class AssetTrendQuery(BaseRuleRequest):
    lfast: NonNegativeInt
    lslow: NonNegativeInt

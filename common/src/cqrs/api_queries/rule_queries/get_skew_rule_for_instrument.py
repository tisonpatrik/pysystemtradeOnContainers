from pydantic import NonNegativeInt

from common.src.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetSkewRuleForInstrumentQuery(RuleRequest):
    speed: NonNegativeInt
    lookback: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/rules_route/get_rule/"

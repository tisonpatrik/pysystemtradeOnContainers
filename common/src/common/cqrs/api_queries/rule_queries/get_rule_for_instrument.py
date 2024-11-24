from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetRuleForInstrumentQuery(RuleRequest):
    speed: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/rules_route/get_rule/"

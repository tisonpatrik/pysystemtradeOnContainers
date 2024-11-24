from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetRelativeCarry(RuleRequest):
    @property
    def url_string(self) -> str:
        return "http://rules:8000/relative_carry_route/get_relative_carry/"

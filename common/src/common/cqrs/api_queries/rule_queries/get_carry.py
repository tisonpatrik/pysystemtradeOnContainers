from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetCarryQuery(RuleRequest):
    smooth_days: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/carry_route/get_carry/"

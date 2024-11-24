from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetAccelQuery(RuleRequest):
    lfast: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/accel_route/get_accel/"

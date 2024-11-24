from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetMomentumQuery(RuleRequest):
    lfast: NonNegativeInt
    lslow: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/momentum_route/get_momentum/"

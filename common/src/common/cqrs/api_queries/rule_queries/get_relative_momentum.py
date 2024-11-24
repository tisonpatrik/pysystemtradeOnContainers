from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetRelativeMomentumQuery(RuleRequest):
    horizon: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/relative_momentum_route/get_relative_momentum/"

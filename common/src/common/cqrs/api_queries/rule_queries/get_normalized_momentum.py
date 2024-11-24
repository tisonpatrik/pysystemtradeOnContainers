from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetNormalizedMomentumQuery(RuleRequest):
    lfast: NonNegativeInt
    lslow: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/normalized_momentum_route/get_normalized_momentum/"

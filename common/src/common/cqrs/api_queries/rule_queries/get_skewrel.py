from pydantic import NonNegativeInt

from common.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetSkewRelQuery(RuleRequest):
    smooth: NonNegativeInt
    lookback: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/skewrel_route/get_skewrel/"

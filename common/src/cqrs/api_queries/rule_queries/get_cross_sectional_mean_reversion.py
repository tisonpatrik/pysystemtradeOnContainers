from pydantic import NonNegativeInt

from common.src.cqrs.api_queries.rule_queries.rule_request import RuleRequest


class GetCrossSectionalMeanReversionQuery(RuleRequest):
    horizon: NonNegativeInt

    @property
    def url_string(self) -> str:
        return "http://rules:8000/cross_sectional_mean_reversion_route/get_cross_sectional_mean_reversion/"

from pydantic import NonNegativeInt, StringConstraints
from typing_extensions import Annotated

from common.src.http_client.requests.fetch_request import FetchRequest


class GetRuleQuery(FetchRequest):
	name: Annotated[str, StringConstraints(max_length=15)]
	speed: NonNegativeInt

	@property
	def url_string(self) -> str:
		return 'http://rules:8000/rules_route/get_rule/'

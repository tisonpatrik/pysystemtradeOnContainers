from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import PositiveFloat, StringConstraints

from common.src.http_client.requests.fetch_request import FetchRequest
from common.src.validation.scaling_type import ScalingType


class RuleRequest(FetchRequest, ABC):
    symbol: Annotated[str, StringConstraints(max_length=30)]
    use_attenuation: bool
    scaling_type: ScalingType
    scaling_factor: PositiveFloat

    @property
    @abstractmethod
    def url_string(self) -> str:
        pass

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class FetchRequest(BaseModel, ABC):
    @property
    @abstractmethod
    def url_string(self) -> str:
        pass

    @property
    def params(self) -> dict[str, Any]:
        return self.model_dump()

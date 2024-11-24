from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class PostRequest(BaseModel, ABC):
    raw_data: dict[str, Any]

    @property
    @abstractmethod
    def url_string(self) -> str:
        pass

    @property
    @abstractmethod
    def data(self) -> dict:
        return self.raw_data

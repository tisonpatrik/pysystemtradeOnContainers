from abc import ABC, abstractmethod


class GetCacheStatement(ABC):
    """Abstract class for encapsulating data fetching key for Redis.
    This class must be extended with specific implementations that format or validate queries."""

    def __init__(self):
        self._key = tuple

    @property
    @abstractmethod
    def key(self) -> str:
        """Abstract property to create specific keys for various types of statements.
        Implementations should define the logic for generating keys that uniquely identify
        cached data based on the parameters of the specific statement."""
        pass

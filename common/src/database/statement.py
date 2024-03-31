from typing import Any, Sequence, Tuple


class Statement:
    def __init__(self, query: str, parameters: Sequence[Any]):
        self._query = query
        self._parameters = tuple(parameters)  # Ensure parameters are stored as a tuple

    @property
    def query(self) -> str:
        """Returns the SQL query string."""
        return self._query

    @property
    def parameters(self) -> Tuple[Any, ...]:
        """Returns the parameters as a tuple."""
        return self._parameters

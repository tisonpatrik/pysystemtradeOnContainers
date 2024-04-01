from typing import Any, Sequence, Tuple, Union


class Statement:
    def __init__(self, query: str, parameters: Union[Any, Sequence[Any]]):
        # If parameters is not already a sequence, make it a tuple with one element
        if isinstance(parameters, Sequence) and not isinstance(parameters, str):
            self._parameters = tuple(parameters)
        else:
            self._parameters = (parameters,)  # Ensure a single item is also stored as a tuple

        self._query = query

    @property
    def query(self) -> str:
        """Returns the SQL query string."""
        return self._query

    @property
    def parameters(self) -> Tuple[Any, ...]:
        """Returns the parameters as a tuple."""
        return self._parameters
